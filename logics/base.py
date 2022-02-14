import json

from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from copy import copy
from typing import Dict, Any


class KokkaiBase:

    HOST = 'http://kokkai.ndl.go.jp/api/1.0/'
    ACCEPT = 'application/json'

    PARAMS = {
        # 'maximumRecords': 1,
        'recordPacking': 'json'
    }

    def query(self, params=Dict) -> str:

        params = {**params, **self.PARAMS}
        params = {
            key: params[key] for key in params if params[key]
        }

        query = '&'.join(
            ['{}={}'.format(key, value) for key, value in params.items()]
        )
        query = "?" + query

        return quote(query)

    def request(self, path: str) -> Any:
        if len(path.split('/')) > 1:
            path = path.replace("/", "")

        url = self.HOST + path
        print("url", url)

        try:
            req = Request(url)
            with urlopen(req) as res:
                res = res.read().decode('utf8')
                # res = res.read()
        except HTTPError as e:
            print('HTTPError: {}'.format(e.reason))
        except URLError as e:
            print('URLError: {}'.format(e.reason))
        else:
            return res

    def convert_to_dict(self, json_text: str) -> Dict:
        results = json.loads(json_text)
        return results

    def check_number_of_records(self, params: Dict) -> bool:
        cache_params = copy(params)
        start_record_num = cache_params["startRecord"]

        cache_params["startRecord"] = 1
        query = self.query(cache_params)
        path = "meeting" + query

        response = self.request(path)
        results = self.convert_to_dict(response)

        max_num = results["numberOfRecords"]
        if max_num >= start_record_num:
            return True
        return False
