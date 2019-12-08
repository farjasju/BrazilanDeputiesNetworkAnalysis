from twarc import Twarc
import csv
import os
import io
import json

from config import API_KEY, API_SECRET, ACCESS_TOKEN, TOKEN_SECRET

OUT_DIR = os.path.join('data', 'deputies_tweets')


def save_json(variable, filename):
    with io.open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(variable, indent=4, ensure_ascii=False))


def fetch_timeline():

    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)

    t = Twarc(API_KEY, API_SECRET, ACCESS_TOKEN, TOKEN_SECRET)

    with open(os.path.join('data', 'deputies_accounts.csv'), mode='r') as list_file:

        reader = csv.DictReader(list_file)

        for deputee in reader:
            user_screen_name = deputee['screen_name']
            print(user_screen_name)
            user_id = deputee['id']
            tweets = []

            if not os.path.exists(os.path.join(
                    OUT_DIR, user_screen_name + '.json')):

                for tweet in t.timeline(user_id=user_id):
                    tweets.append(tweet)

                save_json(tweets, os.path.join(
                    OUT_DIR, user_screen_name + '.json'))


def main():
    fetch_timeline()


if __name__ == '__main__':
    main()
