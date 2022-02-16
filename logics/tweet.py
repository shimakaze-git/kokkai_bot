import os
import tweepy
from dotenv import find_dotenv, load_dotenv

# .envファイルを探して読み込む
env_file = find_dotenv()
load_dotenv(env_file)

# APIキーの設定
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_KEY_SECRET = os.environ.get('ACCESS_KEY_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_KEY_SECRET)

api = tweepy.API(auth)

public_tweets = api.home_timeline()

print("public_tweets", public_tweets)
# for tweet in public_tweets:
#     print(tweet.text)
