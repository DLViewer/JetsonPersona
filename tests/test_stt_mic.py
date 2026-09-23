from pathlib import Path

from jetson_persona.audio.input import USBMicrophoneInput
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

RECORDING_FILE = PROJECT_ROOT / "recording.wav"


def main() -> None:
    print("JetsonPersona Microphone STT Test")
    print()
    print("Speak for 5 seconds...")
    print()

    microphone = USBMicrophoneInput(
        device="plughw:CARD=Audio,DEV=0",
        sample_rate=16000,
        channels=1,
        duration=5,
        output_file=RECORDING_FILE,
    )

    stt = WhisperCppSTT(
        executable=WHISPER_CLI,
        model=WHISPER_MODEL,
        language="auto",
    )

    try:
        audio_file = microphone.record()

        print()
        print(f"Recorded: {audio_file}")
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
