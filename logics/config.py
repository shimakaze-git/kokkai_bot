import os
# import tweepy
from dotenv import find_dotenv, load_dotenv

# .envファイルを探して読み込む
env_file = find_dotenv()
load_dotenv(env_file)

# APIキーの設定
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_KEY_SECRET = os.environ.get('ACCESS_KEY_SECRET')
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
TWITTER_NAME = os.environ.get('TWITTER_NAME')
