from pathlib import Path

import requests

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

LLM_URL = "http://127.0.0.1:8080/v1/chat/completions"


def ask_llm(text: str) -> str:
    payload = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are JetsonPersona, a concise and helpful "
                    "voice assistant."
                ),
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        "temperature": 0.7,
        "max_tokens": 128,
    }

    response = requests.post(
        LLM_URL,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    print("JetsonPersona Voice -> STT -> LLM Test")
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
        use_gpu=False,
    )

    try:
        print("Speak for 5 seconds...")
        print()

        audio_file = microphone.record()

        print()
        print("Transcribing...")

        user_text = stt.transcribe(audio_file)

        print()
        print(f"You: {user_text}")

        if not user_text:
            print("No speech recognised.")
            return

        print()
        print("Thinking...")

        reply = ask_llm(user_text)

        print()
        print(f"JetsonPersona: {reply}")

    except requests.RequestException as exc:
        print()
        print(f"LLM connection error: {exc}")

    except Exception as exc:
        print()
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
