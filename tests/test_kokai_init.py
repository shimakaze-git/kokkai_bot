#!/usr/bin/env python

"""Tests for `kokai_kokkai_init` package."""

# import pytest


from logics.kokai_bot import Kokkai


def test_comment_count_in_mouth():
    # comment = "プログラミング"
    # speaker = "あべしんぞう"

    kokai = Kokkai()

    # results = kokai.meeting(
    #     comment=comment, speaker=speaker, start=290, position=1
    # )
    # print("results", results)

    # records_count = results["numberOfRecords"]
    # print("records_count", records_count)

    # next_position = results["nextRecordPosition"]
    # print("next_position", next_position)

    # maximum = 10


    # meeting_records = results["meetingRecord"]
    meeting_records = []

    comment = "DX"
    speaker = ""

    from_date = ""
    until_date = ""

    count = 1
    count = 14
    count = 15
    # count = 28
    while True:
        # print("---" * 20)

        results = kokai.meeting(
            comment=comment,
            speaker=speaker,
            position=count,
            from_date=from_date,
            until_date=until_date,
        )

        # records_count = results["numberOfRecords"]
        # print("records_count", records_count)

        next_position = results["nextRecordPosition"]
        print("next_position", next_position)

        print("pos", 1 * count)

        meeting_record = results["meetingRecord"]

        meeting_records += meeting_record

        if next_position is None:
            break

        count += 1

    # print("meeting_records", len(meeting_records))

    import collections

    speakers = []
    speechs = []
    for m in meeting_records:
        speech_record = m["speechRecord"]
        # speech = speech_record["speech"]

        for sr in speech_record:
            # speech = sr
            speaker = sr["speaker"]
            speech = sr["speech"]

            speakers.append(speaker)
            speechs.append(speech)

        # print("m", "speech" in speech_record)
        print("--" * 30)
    
    # print("speakers", speakers)
    counter = collections.Counter(speakers)
    print("counter", counter)
    # print("most_common", counter.most_common())

    speaker = "萩生田光一"
    print([s for s in speakers if s == speaker])
