from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


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
    USB microphone input.

    Hardware implementation will be completed/tested
    when the USB audio device is available.
    """

    def __init__(
        self,
        device=None,
        sample_rate: int = 16000,
        channels: int = 1,
    ) -> None:
        self.device = device
        self.sample_rate = sample_rate
        self.channels = channels

    def record(self) -> Path:
        raise NotImplementedError(
            "USB microphone recording is not enabled yet."
        )
