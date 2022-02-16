import calendar
import itertools

from datetime import datetime, timedelta, date

# from logics.kokkai_bot import Kokkai
from logics.utils import get_nth_dow, get_nth_week, get_weekday
from logics.kokkai_bot import (
    get_meeting_records,
    get_list_counter,
    speechs_cleanning,
    get_nouns_in_speechs
)

def main(comment, speaker, from_date, until_date):
    # comment = "DX"
    # comment = ""
    # speaker = ""

    # from_date = "2022-01-01"
    # until_date = "2022-01-31"

    meeting_records = get_meeting_records(
        comment, speaker, from_date, until_date
    )

    speakers = []
    speechs = []
    groups = []

    for m in meeting_records:
        speech_record = m["speechRecord"]
        # speech = speech_record["speech"]

        for sr in speech_record:
            # speech = sr
            speaker = sr["speaker"]
            speech = sr["speech"]
            group = sr["speakerGroup"]

            speakers.append(speaker)
            speechs.append(speech)

            groups.append(group)

        # print("m", "speech" in speech_record)
    print("--" * 30)
    
    # print("speakers", speakers)
    speakers_counter = get_list_counter(speakers)
    top_speakers = speakers_counter.most_common()[:10]
    print("top_speakers", top_speakers)

    groups_counter = get_list_counter(groups)
    print("groups_counter", groups_counter)

    speechs = speechs_cleanning(speechs)

    print("speechs", len(speechs))

    nouns_list = get_nouns_in_speechs(speechs)
    print("nouns_list", len(nouns_list))

    nouns_list_from_iterable = list(
        itertools.chain.from_iterable(nouns_list)
    )
    print("nouns_list_from_iterable length", len(nouns_list_from_iterable))
    # groups_counter = get_list_counter(groups)

    # print("nouns_list_from_iterable", nouns_list_from_iterable)
    nouns_list_from_iterable_counter = get_list_counter(
        nouns_list_from_iterable
    )
    # print("nouns_list_from_iterable_counter", nouns_list_from_iterable_counter)
    top_nouns_list = nouns_list_from_iterable_counter.most_common()[:10]
    print("top_nouns_list", top_nouns_list)

    # 全ての議員たちが5位以内の頻度もある単語を何回言ったかを集計
    all_count_words = {}

    # 発言数が5位以内の議員たちが5位以内の頻度もある単語を何回言ったかを集計
    rank_words = {}
    for _, s in enumerate(top_speakers):
        # print(i, s[0])

        speaker_name = s[0]
        speakers_idx = [
            i for i, s in enumerate(speakers) if s == speaker_name
        ]

        nouns_from_speaker = [
            nouns_list[idx] for idx in speakers_idx
        ]

        for top_word in top_nouns_list:
            for nouns in nouns_from_speaker:
                # print("nouns", top_word, nouns)

                word = top_word[0]
                if word in nouns:
                    # rank_words[speaker_name] += 1
                    if speaker_name in rank_words:

                        if word in rank_words[speaker_name]:
                            rank_words[speaker_name][word] += 1
                        else:
                            rank_words[speaker_name][word] = 1
                        # rank_words[speaker_name] += 1
                    else:
                        rank_words[speaker_name] = {}

                    # all_count_words
                    if speaker_name in all_count_words:
                        all_count_words[speaker_name] += 1
                    else:
                        all_count_words[speaker_name] = 1

    print("rank_words", rank_words)

    # print("会議録情報", "会議録情報" in speakers)

    # 会議録情報というspeakerが多いので削除する
    if "会議録情報" in all_count_words:
        all_count_words.pop("会議録情報")

    # print("speakers : all_rank_words", all_rank_words)
    print("speakers : all_count_words", all_count_words)
    sorted_all_count_words = sorted(
        all_count_words.items(),
        key=lambda i: i[1],
        reverse=True
    )
    print("sorted_all_count_words", sorted_all_count_words)

def check_range_data(comment, speaker, from_date, until_date):
    meeting_records = get_meeting_records(
        comment, speaker, from_date, until_date
    )

    date_list = [
        meeting["date"] for meeting in meeting_records
    ]
    # print("date_list", date_list)

    if (from_date in date_list) and (until_date in date_list):
        return True
    return False

def check_week_run_before(input_date):
    print("check_week_run", input_date)

    # datetime
    tdate = datetime.strptime(input_date, '%Y-%m-%d').date()

    # 4週間前の日
    before_date = tdate - timedelta(days=28)

    # 週初めの日
    from_date = before_date - timedelta(days=7)

    # 週最後の日
    until_date = before_date - timedelta(days=1)

    return from_date, until_date

# if __name__ == "__main__":
#     main()
