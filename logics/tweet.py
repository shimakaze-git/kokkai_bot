import tweepy
import twitter
import requests
import json
import time

from config import (
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_KEY,
    ACCESS_KEY_SECRET,
    BEARER_TOKEN,
    TWITTER_NAME
)


class Tweet:
    def __init__(self):
        auth = tweepy.OAuthHandler(
            CONSUMER_KEY, CONSUMER_SECRET
        )
        auth.set_access_token(
            ACCESS_KEY, ACCESS_KEY_SECRET
        )
        self.api = tweepy.API(auth)
        print("self.api", self.api)

        # OAuthの認証オブジェクトの作成
        self.oauth = twitter.OAuth(
            ACCESS_KEY,
            ACCESS_KEY_SECRET,
            CONSUMER_KEY,
            CONSUMER_SECRET,
        )

        self.twitter = twitter.Twitter(
            auth=self.oauth
        )

    def tweet(self, text: str, account=""):
        # self.api.update_status(text)

        tweet_text = "{0}".format(text)
        if account:
            tweet_text = "@{0} ".format(account) + tweet_text

        self.twitter.statuses.update(
            status=tweet_text
        )

    def image_tweet(self, text: str, file_path: str):
        self.api.update_status_with_media(
            status=text,
            filename=file_path
        )

    def images_tweet(self, text: str, file_path_list: list):
        media_ids = []
        for file_path in file_path_list:
            res = self.api.media_upload(file_path)
            media_ids.append(
                res.media_id
            )

        # tweet with multiple images
        self.api.update_status(
            status=text,
            media_ids=media_ids
        )


class TweetStream(Tweet):
    def __init__(self):
        super(TweetStream, self).__init__()

        self.stream = twitter.TwitterStream(
            auth=self.oauth
        )


    def bearer_oauth(self, req):
        req.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
        # req.headers["User-Agent"] = "v2FilteredStreamPython"
        return req

    def get_rules(self):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_oauth
        )

        if response.status_code != 200:
            raise Exception(
                "Cannot get rules (HTTP {}): {}".format(
                    response.status_code,
                    response.text
                )
            )
        print(response.json())
        print("---" * 20)
        print(json.dumps(response.json()))
        return response.json()

    def set_rules(self):
        rules = [
            {
                "value":"to:{0}".format(TWITTER_NAME)
            }
        ]
        payload = {
            "add": rules
        }

        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_oauth,
            json=payload,
        )
        if response.status_code != 201:
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
            )
        print(json.dumps(response.json()))

    def get_stream(self):
        status = True
        while status:
            # time.sleep(1)
            try:
                with requests.get(
                    "https://api.twitter.com/2/tweets/search/stream",
                    auth=self.bearer_oauth,
                    stream=True,
                ) as response:
                    print("status_code", response.status_code)
                    if response.status_code != 200:
                        raise Exception(
                            "Cannot get stream (HTTP {}): {}".format(
                                response.status_code, response.text
                            )
                        )
                    for response_line in response.iter_lines():
                        print("response_line", response_line)
                        if response_line:
                            json_response = json.loads(response_line)

                            # ツイートID
                            tweet_id = json_response["data"]["id"]

                            # 相手の送ってきた内容
                            reply_text=json_response["data"]["text"]

                            print("tweet_id", tweet_id)
                            print("reply_text", reply_text)

                            # ここで自分のリプライの内容を設定します
                            text ="リプライありがとう!"

                            print(text)
                            # print("tweet_id", tweet_id)
                            # Client.create_tweet(
                            #     text=text,
                            #     in_reply_to_tweet_id =tweet_id)

            # except ChunkedEncodingError as chunkError:
            #     print(traceback.format_exc())
            #     time.sleep(6)
            #     continue
            
            # except ConnectionError as e:
            #     print(traceback.format_exc())
            #     run+=1
            #     if run <10:
            #         time.sleep(6)
            #         print("再接続します",run+"回目")
            #         continue
            #     else:
            #         run=0

            except Exception as e:
                # some other error occurred.. stop the loop
                print("Stopping loop because of un-handled error")
                # print(traceback.format_exc())

                status = False

stream = TweetStream()

stream.tweet(
    text="ツイート!!", account="shimakaze_soft"
)

# 監視する対象の文字列
tracking_text = '@{0}'.format(TWITTER_NAME)

# for tweet in stream.stream.statuses.filter(language='ja', track=tracking_text):
#     print(tweet)

# https://qiita.com/YiwaiY/items/7148389e3d76e61b798d