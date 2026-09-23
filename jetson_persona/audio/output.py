from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
import subprocess

class AudioOutput(ABC):
    """Base interface for JetsonPersona audio output."""

    @abstractmethod
    def play(self, audio_file: str | Path) -> None:
        """
        Play an audio file.
        """
        raise NotImplementedError


class FileAudioOutput(AudioOutput):
    """
    Development audio output.

    Validates an audio file without requiring physical
    speaker or headphone hardware.
    """

    def play(self, audio_file: str | Path) -> None:
        audio_file = Path(audio_file)

        if not audio_file.is_file():
            raise FileNotFoundError(
                f"Audio output file not found: {audio_file}"
            )

        print(f"Audio output ready: {audio_file}")


class USBAudioOutput(AudioOutput):
    """
    USB speaker/headphone output using ALSA aplay.

    Default device:
        AB17X USB Audio
    """

    def __init__(
        self,
        device: str = "plughw:CARD=Audio,DEV=0",
    ) -> None:
        self.device = device

    def play(self, audio_file: str | Path) -> None:
        audio_file = Path(audio_file)

        if not audio_file.is_file():
            raise FileNotFoundError(
                f"Audio output file not found: {audio_file}"
            )

        command = [
            "aplay",
            "-D",
            self.device,
            str(audio_file),
        ]

        try:
            subprocess.run(
                command,
                check=True,
            )

        except FileNotFoundError as exc:
            raise RuntimeError(
                "aplay is not installed."
            ) from exc

        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                f"Audio playback failed with exit code "
                f"{exc.returncode}"
            ) from exc
