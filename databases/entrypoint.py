import json
import os
import time
from datetime import datetime
from multiprocessing import Process
from os import path

import schedule
from dotenv import load_dotenv
from flask import Flask, abort, jsonify

from collection import iterate_notion_collection

load_dotenv()

COLLECTIONS = {
    'coffee': 'https://www.notion.so/f213/f1611b83a8664185b19be85c936fb64e?v=82a5aa580ab94b788aec31c648b0fd36',
}

STORAGE_DIR = os.getenv('STORAGE_DIR') or '.'


def fetch(collection, url):
    with open(path.join(STORAGE_DIR, f'{collection}.json'), 'w') as collection_file:
        json.dump(
            obj=list(iterate_notion_collection(url)),
            fp=collection_file,
            ensure_ascii=False,
            default=lambda val: val.isoformat() if isinstance(val, datetime) else None,
        )


def fetch_all():
    for collection, url in COLLECTIONS.items():
        fetch(collection, url)


def run_scheduler():
    schedule.every().hour.do(fetch_all)

    while True:
        schedule.run_pending()
        time.sleep(1)


web = Flask(__name__)


@web.route('/collections/<collection>')
def get_collection(collection):
    try:
        with open(path.join(STORAGE_DIR, f'{collection}.json'), 'r') as collection_file:
            return jsonify(json.load(collection_file))

    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    print('Doing crawl for the first time...')
    fetch_all()  # do crawling at the first run

    print('Running web server...')
    flask = Process(target=lambda: web.run(host='0.0.0.0'))
    flask.start()

    print('Running the main loop...')
    scheduler = Process(target=run_scheduler)
    scheduler.start()

    flask.join()
    scheduler.join()
