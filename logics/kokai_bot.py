"""Main module."""
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
