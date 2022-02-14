"""Main module."""
import itertools
import collections
import MeCab

from .base import KokkaiBase
# from .speech import SpeechRecordList
# from .meeting import MeetingRecordList

from .utils import convert_group_name

# from typing import Optional, List
from typing import List


class Kokkai(KokkaiBase):
    '''
    '''

    def __init__(self):
        # self.speech_records: Optional[SpeechRecordList] = None
        # self.meeting_records: Optional[MeetingRecordList] = None
        self.meeting_records = None

    def meeting(
        self,
        comment="",
        speaker="",
        maximum=10,
        start=1,
        position=1,
        from_date="2022-01-01",
        until_date="2022-01-31"
    ) -> List[str]:
        # print("---" * 30)

        start_pos = start + (maximum * (position - 1))
        # print("start_pos", start_pos, start, position, maximum * (position - 1))

        # speech_list = []

        results = {}

        params = {
            'any': comment,
            # 'speaker': speaker,
            'startRecord': start_pos,
            'maximumRecords': maximum,
            "from": from_date,
            "until": until_date,
        }
        if self.check_number_of_records(params):
            query = self.query(params)
            path = "meeting" + query

            response = self.request(path)
            results = self.convert_to_dict(response)

        return results

def speechs_cleanning(speechs):

    clean_speechs = []
    for speech in speechs:
        # print(speech)

        speech_text = speech

        # 文字列の先頭と末尾の空白を削除
        # speech_text = speech_text.strip()

        # 文字列の先頭の空白を削除
        # speech_text = speech_text.lstrip()

        # 文字列の末尾の空白を削除
        # speech_text = speech_text.rstrip()

        # print("____", [s for s in speech_text[:20]])

        for i, s in enumerate(speech_text):
            # print("s", s, i)
            if s == "\u3000":
                speech_text = speech_text[i+1:]
                break

        #\u3000は全角スペース
        # text = "a\u3000 b\t\nc\r\n"
        # 改行コード、タブ、スペースなどをまとめて削除
        speech_text = ''.join(speech_text.split())

        speech_text = ''.join(speech_text.splitlines())

        # print(speech_text)

        clean_speechs.append(speech_text)

        # print(speech_text)
        # print("---" * 30)

    return clean_speechs

def get_meeting_records(comment, speaker, from_date, until_date):

    kokai = Kokkai()

    # meeting_records = results["meetingRecord"]
    meeting_records = []

    comment = "DX"
    speaker = ""

    from_date = ""
    until_date = ""

    count = 1
    # count = 14
    # count = 15
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

        # print("next_position", next_position)
        # print("pos", 1 * count)

        meeting_record = results["meetingRecord"]

        meeting_records += meeting_record

        if next_position is None:
            break

        count += 1

    return meeting_records
    # print("meeting_records", len(meeting_records))

mecab = MeCab.Tagger ("-Ochasen")

def text_parse(text):
    return mecab.parse(text)
    # print(mecab.parse(text))

def get_list_counter(list_data):
    counter = collections.Counter(list_data)
    return counter

def get_nouns_in_speechs(speechs):

    nouns_list = []
    for s in speechs:

        nouns = [
            line.split()[0] for line in text_parse(s).splitlines()
            if "名詞" in line.split()[-1].split("-")[0]
            if not ("名詞-数" in line.split()[-1])

            # line for line in text_parse(s).splitlines()
            # if "名詞" in line.split()[-1]
        ]

        # print(nouns)

        # print(text_parse(s))
        # print(s, text_parse(s))

        nouns_list.append(nouns)

        # print("---" * 20)
    return nouns_list

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
    print("speakers_counter", speakers_counter)
    # print("most_common", speakers_counter.most_common())

    # speaker = "萩生田光一"
    # print([i for i, s in enumerate(speakers) if s == speaker])

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
    print("nouns_list_from_iterable_counter", nouns_list_from_iterable_counter)
