import os

from dotenv import load_dotenv
from notion.client import NotionClient

load_dotenv(verbose=True)

notion = NotionClient(token_v2=os.getenv('NOTION_TOKEN'))

def _get_row_dict(row) -> dict:
    return {prop: getattr(row, prop) for prop in row._get_property_slugs()}


def iterate_notion_collection(url):
    collection_view = notion.get_collection_view(url)

    for row in collection_view.collection.get_rows():
        yield _get_row_dict(row)


__all__ = [
    iterate_notion_collection,
]
