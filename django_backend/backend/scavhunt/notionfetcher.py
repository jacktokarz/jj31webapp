# from scavhunt.fetcher import Fetcher
from notion_client import Client
import os

with open(os.curdir + "/etc/notion_key.txt") as f:
    notion_key = f.read().strip()
notion = Client(auth=notion_key)