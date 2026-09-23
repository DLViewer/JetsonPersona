from __future__ import annotations

import subprocess
from pathlib import Path


class SpeechToTextError(RuntimeError):
    """Raised when speech-to-text processing fails."""


class WhisperCppSTT:
    """
    Speech-to-text backend using whisper.cpp.

    This class does not access the microphone directly.
    It accepts an existing audio file and returns recognised text.
    """

    def __init__(
        self,
        executable: str | Path,
        model: str | Path,
        language: str = "auto",
        use_gpu: bool = True,
    ) -> None:
        self.executable = Path(executable)
        self.model = Path(model)
        self.language = language
        self.use_gpu = use_gpu

    def validate(self) -> None:
        """Check that whisper.cpp executable and model exist."""

        if not self.executable.is_file():
            raise SpeechToTextError(
                f"whisper.cpp executable not found: {self.executable}"
            )

        if not self.model.is_file():
            raise SpeechToTextError(
                f"Whisper model not found: {self.model}"
            )

    def transcribe(
        self,
        audio_file: str | Path,
        language: str | None = None,
    ) -> str:
        """Transcribe an audio file and return recognised text."""

        audio_file = Path(audio_file)

        if not audio_file.is_file():
            raise SpeechToTextError(
                f"Audio file not found: {audio_file}"
            )

        self.validate()

        selected_language = language or self.language

        command = [
            str(self.executable),
            "-m",
            str(self.model),
            "-f",
            str(audio_file),
            "-l",
            selected_language,
            "--no-timestamps",
        ]

        if not self.use_gpu:
            command.append("--no-gpu")

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
            )

        except subprocess.CalledProcessError as exc:
            raise SpeechToTextError(
                f"whisper.cpp failed:\n{exc.stderr}"
            ) from exc

        return result.stdout.strip()
