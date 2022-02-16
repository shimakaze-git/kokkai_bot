"""Main module."""
import itertools
import collections
import MeCab
from pyparsing import Word

from .base import KokkaiBase
# from .speech import SpeechRecordList
# from .meeting import MeetingRecordList

from .utils import convert_group_name, filter_word

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

    # comment = "DX"
    # speaker = ""

    # from_date = ""
    # until_date = ""

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
        print("next_position", next_position)
        # print("pos", 1 * count)

        meeting_record = results["meetingRecord"]

        meeting_records += meeting_record

        print("count", count, next_position)
        if next_position is None:
            break

        count += 1

    return meeting_records
    # print("meeting_records", len(meeting_records))

# mecab = MeCab.Tagger ("-Ochasen")
mecab = MeCab.Tagger(
    "-d /var/lib/mecab/dic/mecab-ipadic-neologd"
)

def text_parse(text):
    return mecab.parse(text)
    # print(mecab.parse(text))

def get_list_counter(list_data):
    counter = collections.Counter(list_data)
    return counter

def get_nouns_in_speechs(speechs):

    nouns_list = []
    for s in speechs:

        parts = ["名詞"]

        # part_options = ["非自立", "数", "代名詞", "接尾"]
        # part_options = ["固有名詞", "一般"]
        part_options = ["固有名詞"]

        nouns = []

        node = mecab.parseToNode(s)
        while node:
            # 単語を取得
            if node.feature.split(",")[6] == '*':
                word = node.surface
            else:
                word = node.feature.split(",")[6]

            # 品詞を取得
            part = node.feature.split(",")[0]

            # 品詞のオプションを取得
            part_option = node.feature.split(",")[1]

            # if (part in parts) and (part_option not in part_options):
            if (
                (part in parts) and \
                (part_option in part_options) and \
                (filter_word(word))
            ):
                nouns.append(word)
            node = node.next

        nouns_list.append(nouns)

        # print("---" * 20)
    return nouns_list
