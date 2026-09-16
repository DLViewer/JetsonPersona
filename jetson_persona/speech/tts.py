from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class TextToSpeechError(RuntimeError):
    """Raised when text-to-speech processing fails."""


class TextToSpeech(ABC):
    """Base interface for JetsonPersona text-to-speech."""

    @abstractmethod
    def synthesize(
        self,
        text: str,
        output_file: str | Path,
    ) -> Path:
        """
        Convert text into an audio file.

        Returns
        -------
        Path
            Path to the generated audio file.
        """
        raise NotImplementedError
