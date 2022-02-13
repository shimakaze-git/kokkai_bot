from logics.kokai_bot import Kokkai


def main():
    comment = "プログラミング"
    speaker = "あべしんぞう"

    kokai = Kokkai()
    kokai.meeting(
        comment=comment, speaker=speaker, start=1, position=1
    )

if __name__ == "__main__":
    main()
