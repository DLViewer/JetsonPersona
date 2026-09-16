from pathlib import Path

from jetson_persona.audio.input import FileAudioInput
from jetson_persona.speech.stt import WhisperCppSTT


PROJECT_ROOT = Path(__file__).resolve().parents[1]

WHISPER_CLI = (
    PROJECT_ROOT
    / "external"
    / "whisper.cpp"
    / "build"
    / "bin"
    / "whisper-cli"
)

WHISPER_MODEL = (
    PROJECT_ROOT
    / "models"
    / "speech"
    / "ggml-base.bin"
)


def main() -> None:
    print("JetsonPersona Speech-to-Text Test")
    print()

    audio_path = input("Audio WAV file: ").strip()

    if not audio_path:
        print("No audio file specified.")
        return

    audio_input = FileAudioInput(audio_path)

    stt = WhisperCppSTT(
        executable=WHISPER_CLI,
        model=WHISPER_MODEL,
        language="auto",
    )

    try:
        audio_file = audio_input.record()

        print()
        print(f"Audio: {audio_file}")
        print("Language: auto")
        print("Transcribing...")

        text = stt.transcribe(audio_file)

    except Exception as exc:
        print()
        print(f"Error: {exc}")
        return

    print()
    print(f"Recognised: {text}")


if __name__ == "__main__":
    main()
