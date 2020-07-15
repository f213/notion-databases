import json
import os
import time
from datetime import datetime
from os import path

import schedule
from dotenv import load_dotenv

from collection import iterate_notion_collection

load_dotenv()

COLLECTIONS = {
    'coffee': 'https://www.notion.so/f213/f1611b83a8664185b19be85c936fb64e?v=82a5aa580ab94b788aec31c648b0fd36',
}


def fetch(collection, url):
    storage_dir = os.getenv('STORAGE_DIR') or '.'
    with open(path.join(storage_dir, f'{collection}.json'), 'w') as collection_file:
        json.dump(
            obj=list(iterate_notion_collection(url)),
            fp=collection_file,
            ensure_ascii=False,
            default=lambda val: val.isoformat() if isinstance(val, datetime) else None,
        )


def fetch_all():
    for collection, url in COLLECTIONS.items():
        fetch(collection, url)


if __name__ == '__main__':
    fetch_all()  # do crawling at the first run

    schedule.every().hour.do(fetch_all)

    while True:
        schedule.run_pending()
        time.sleep(1)
