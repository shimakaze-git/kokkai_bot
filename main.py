import pprint
import collections

import MeCab
import csv
from datetime import datetime, timedelta

# from kokkai_bot import 
from logics.kokkai_bot import Kokkai, get_meeting_records
from logics.utils import convert_group_name, filter_word

mecab = MeCab.Tagger(
    "-d /var/lib/mecab/dic/mecab-ipadic-neologd"
)

kokkai = Kokkai()

def date_convert(date):
    month = str(date.month)
    if int(date.month) < 10:
        month = '0' + str(date.month)

    day = str(date.day)
    if int(date.day) < 10:
        day = '0' + str(date.day)

    return str(date.year) + '-' + month + '-' + day

def speech_cleanning(speech_text):
    # print('speech_text', speech_text)

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
    return speech_text

def get_nouns_in_speechs(speech):

    parts = ["名詞"]

    # part_options = ["非自立", "数", "代名詞", "接尾"]
    part_options = ["一般"]
    # part_options = ["固有名詞", "一般"]
    # part_options = ["固有名詞"]

    nouns = []

    node = mecab.parseToNode(speech)
    while node:
        # print('node.feature', node.feature.split(",")[6])

        # 単語を取得
        if node.feature.split(",")[6] == '*':
            word = node.surface
        else:
            word = node.feature.split(",")[6]

        # 品詞を取得
        part = node.feature.split(",")[0]

        # 品詞のオプションを取得
        part_option = node.feature.split(",")[1]

        # print('part', part, part_option, word)

        # if (part in parts) and (part_option not in part_options):
        if (
            (part in parts) and \
            (part_option in part_options) and \
            (filter_word(word))
        ):
            nouns.append(word)
        node = node.next
    return nouns

def speechs(speechRecords):

    nouns_list = []

    for record in speechRecords:
        speaker = record['speaker']
        speaker_yomi = record['speakerYomi']
        speaker_group = record['speakerGroup']
        speaker_position = record['speakerPosition']
        speaker_role = record['speakerRole']

        data = {}

        if speaker != '会議録情報':
            speech = record['speech']
            # print('_', speaker, speaker_group, speaker_position, speaker_role)

            clean_speech = speech_cleanning(speech)
            # print('clean_speech', clean_speech)

            nouns = get_nouns_in_speechs(clean_speech)
            # print('nouns', nouns)

            data['speaker'] = speaker
            data['speaker_yomi'] = speaker_yomi
            data['speaker_group'] = speaker_group
            data['speaker_position'] = speaker_position
            data['nouns'] = nouns
            data['speech'] = clean_speech

            nouns_list.append(data)
    return nouns_list

if __name__ == "__main__":

    with open('history.csv') as f:
        reader = csv.reader(f)
        lines = [row for row in reader]

        last = len(lines)
        issue_ids = [l[0] for l in lines[1:]]
        last_date = lines[last-1][3]
        last_date = last_date.split('-')
        last_date = datetime(
            int(last_date[0]), int(last_date[1]), int(last_date[2]), 0, 0, 0, 0
        )

        now = datetime.now()
        # now = datetime(
        #     2022, 4, 5, 0, 0, 0, 0
        # )

        diff = (now - last_date).days

        diff_days = [i+1 for i in range(diff)]
        date_list = [last_date]
        date_list += [last_date + timedelta(days=day) for day in diff_days]
        date_list = [date_convert(date) for date in date_list]

    meeting_records_list = []
    get_issue_ids = []
    for date in date_list:
        comment=""
        speaker=""
        position=1
        # from_date="2022-04-05"
        # until_date="2022-04-05"
        from_date=date
        until_date=date

        meeting_records = get_meeting_records(
            comment=comment,
            speaker=speaker,
            from_date=from_date,
            until_date=until_date
        )
        meeting_records_list += meeting_records

        get_issue_ids += [r["issueID"] for r in meeting_records]

    # print(len(meeting_records_list), len(get_issue_ids))
    # print('get_issue_ids', get_issue_ids)

    get_issue_ids_num = [i for i in range(len(get_issue_ids))]
    for id in issue_ids:
        if id in get_issue_ids:
            get_issue_ids_num.remove(
                get_issue_ids.index(id)
            )

    output_csv_list = []

    # 会議録毎に分ける
    for i in get_issue_ids_num:
        m = meeting_records_list[i]
        speech_record = m["speechRecord"]

        parse_meeting_records = speechs(speech_record)

        # print(m['imageKind'])
        # print(m['nameOfHouse'])
        # print(m['nameOfMeeting'])
        # print(m['date'])

        political_party_list = {}
        nouns_list = []
        for m_record in parse_meeting_records:
            nouns = m_record['nouns']
            speaker = m_record['speaker']
            speaker_group = m_record['speaker_group']
            speaker_position = m_record['speaker_position']

            political_party = '非議員'
            if speaker_group:
                political_party = speaker_group.split('・')[0]

            # print('political_party', political_party)
            # political_party_list[political_party] += nouns

            if not (political_party in political_party_list):
                political_party_list[political_party] = []
                political_party_list[political_party] += nouns
            else:
                political_party_list[political_party] += nouns

            print(
                'm_record nouns',
                speaker, speaker_group, speaker_position, political_party, nouns
            )
            # print(political_party, political_party_list[political_party])

            nouns_list += nouns

        # 会議録毎に単語をカウントする
        all_nouns_counter = collections.Counter(nouns_list)
        # print('all_nouns_counter', all_nouns_counter)

        # 政党毎に単語をカウントする
        for p_nouns_key in political_party_list:
            p_nouns_counter = collections.Counter(political_party_list[p_nouns_key])
            political_party_list[p_nouns_key] = p_nouns_counter

        output_csv_list.append(
            [m["issueID"], m["nameOfHouse"], m["nameOfMeeting"], date]
        )
        # print('||------' * 20)

    with open("history.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(output_csv_list)
