from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


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
    Placeholder for future USB speaker/headphone support.

    Hardware implementation will be completed and tested
    when the USB audio device is available.
    """

    def __init__(self, device: str | int | None = None) -> None:
        self.device = device

    def play(self, audio_file: str | Path) -> None:
        raise NotImplementedError(
            "USB audio playback is not implemented yet."
        )
