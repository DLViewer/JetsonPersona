from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
import subprocess

class AudioInput(ABC):
    """Base interface for JetsonPersona audio input."""

    @abstractmethod
    def record(self) -> Path:
        """
        Record audio and return the path to the recorded file.
        """
        raise NotImplementedError


class FileAudioInput(AudioInput):
    """
    Development audio source.

    Allows JetsonPersona to use an existing WAV file instead
    of a physical microphone.
    """

    def __init__(self, audio_file: str | Path) -> None:
        self.audio_file = Path(audio_file)

    def record(self) -> Path:
        if not self.audio_file.is_file():
            raise FileNotFoundError(
                f"Audio file not found: {self.audio_file}"
            )

        return self.audio_file

class USBMicrophoneInput(AudioInput):
    """
    USB microphone input using ALSA arecord.

    Default device:
        AB17X USB Audio

    Recording format:
        16 kHz
        mono
        signed 16-bit PCM WAV

    This format is suitable for whisper.cpp.
    """

    def __init__(
        self,
        device: str = "plughw:CARD=Audio,DEV=0",
        sample_rate: int = 16000,
        channels: int = 1,
        duration: int = 5,
        output_file: str | Path = "recording.wav",
    ) -> None:
        self.device = device
        self.sample_rate = sample_rate
        self.channels = channels
        self.duration = duration
        self.output_file = Path(output_file)

    def record(self) -> Path:
        command = [
            "arecord",
            "-D",
            self.device,
            "-f",
            "S16_LE",
            "-r",
            str(self.sample_rate),
            "-c",
            str(self.channels),
            "-d",
            str(self.duration),
            str(self.output_file),
        ]

        try:
            subprocess.run(
                command,
                check=True,
            )

        except FileNotFoundError as exc:
            raise RuntimeError(
                "arecord is not installed."
            ) from exc

        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                f"Audio recording failed with exit code "
                f"{exc.returncode}"
            ) from exc

        if not self.output_file.is_file():
            raise RuntimeError(
                f"Recording file was not created: "
                f"{self.output_file}"
            )

        return self.output_file
