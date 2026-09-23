from pathlib import Path

from jetson_persona.audio.output import USBAudioOutput


TEST_AUDIO = Path.home() / "test_mic.wav"


def main() -> None:
    print("JetsonPersona USB Audio Output Test")
    print()

    speaker = USBAudioOutput(
        device="plughw:CARD=Audio,DEV=0",
    )

    try:
        print(f"Playing: {TEST_AUDIO}")
        speaker.play(TEST_AUDIO)

    except Exception as exc:
        print()
        print(f"Error: {exc}")
        return

    print()
    print("Playback completed.")


if __name__ == "__main__":
    main()
