from scavhunt.fetcher import Fetcher
from notion_client import Client, AsyncClient
import scavhunt.local_schema as sc
import scavhunt.leaderboard as lb
import os
import threading as th
import time
from queue import Queue, LifoQueue

with open(os.path.dirname(os.path.realpath(__file__)) + "/etc/notion_key.txt") as f:
    notion_key = f.read().strip()
notion = Client(auth=notion_key)
anotion = AsyncClient(auth=notion_key)


print("Starting up!")

class NotionFetcher(Fetcher):

    def __init__(self):
        self.team_result = {
        'object': 'list', 
        'results': [{
            'object': 'page', 
            'id': '1f0212ab-8856-803c-af2b-f19064ed2fc3', 
            'created_time': '2025-05-11T22:42:00.000Z', 
            'last_edited_time': '2025-05-11T22:46:00.000Z', 
            'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 
            'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 
            'cover': None, 
            'icon': None, 
            'parent': {'type': 'database_id', 'database_id': '1ed212ab-8856-80ec-85ee-d3c8d79109c0'}, 
            'archived': False, 
            'in_trash': False, 
            'properties': {
                'Completed Cards': {'id': '%3AiFg', 'type': 'relation', 'relation': [{'id': '1f0212ab-8856-80e6-905f-da800fad1b3b'}], 'has_more': False}, 
                'Favorite Cards': {'id': 'SI_B', 'type': 'relation', 'relation': [{'id': '1f0212ab-8856-80f2-8160-e650f5ab409a'}, {'id': '1f0212ab-8856-80c4-8590-dd06d0a4cd60'}], 'has_more': False}, 
                'Points': {'id': 'f_%3AA', 'type': 'number', 'number': 50}, 
                'Asked Questions': {'id': 'iy%3Ed', 'type': 'relation', 'relation': [{'id': '1e6212ab-8856-803d-ac75-fbbcd7d3c58e'}, {'id': '1e6212ab-8856-8084-91a3-d5f6f705af67'}], 'has_more': False}, 
                'Players': {'id': 'qpuY', 'type': 'relation', 'relation': [{'id': '1f0212ab-8856-809d-bc03-ddc1082c59fa'}, {'id': '1f0212ab-8856-801b-bae3-e8a1ad3c4d2b'}, {'id': '1f0212ab-8856-8087-8b62-d409ebdf66a9'}, {'id': '1f0212ab-8856-8086-9216-e2fd27451d32'}], 'has_more': False}, 
                'Name': {
                    'id': 'title', 
                    'type': 'title', 
                    'title': [{
                        'type': 'text', 
                        'text': {'content': 'Wandas', 'link': None}, 
                        'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 
                        'plain_text': 'Wandas', 'href': None}]}
                }, 
                'url': 'https://www.notion.so/Wandas-1f0212ab8856803caf2bf19064ed2fc3', 'public_url': None}, {'object': 'page', 'id': '1f0212ab-8856-807b-acfd-f3a8c7b45b53', 'created_time': '2025-05-11T22:19:00.000Z', 'last_edited_time': '2025-05-11T22:46:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1ed212ab-8856-80ec-85ee-d3c8d79109c0'}, 'archived': False, 'in_trash': False, 'properties': {'Completed Cards': {'id': '%3AiFg', 'type': 'relation', 'relation': [{'id': '1f0212ab-8856-80c4-8590-dd06d0a4cd60'}], 'has_more': False}, 'Favorite Cards': {'id': 'SI_B', 'type': 'relation', 'relation': [{'id': '1f0212ab-8856-80e6-905f-da800fad1b3b'}], 'has_more': False}, 'Points': {'id': 'f_%3AA', 'type': 'number', 'number': 90}, 'Asked Questions': {'id': 'iy%3Ed', 'type': 'relation', 'relation': [{'id': '1e6212ab-8856-8064-b68a-c7a1c2ec3832'}, {'id': '1e6212ab-8856-8050-942f-decc3a933634'}], 'has_more': False}, 'Players': {'id': 'qpuY', 'type': 'relation', 'relation': [{'id': '1f0212ab-8856-809f-a6ec-e6a9b5a9ca0e'}, {'id': '1f0212ab-8856-800d-978e-dae17833c9a2'}, {'id': '1f0212ab-8856-803c-93ee-f82f67c5502f'}, {'id': '1f0212ab-8856-805e-8144-d055db0ed580'}], 'has_more': False}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Mushrooms', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Mushrooms', 'href': None}]}}, 'url': 'https://www.notion.so/Mushrooms-1f0212ab8856807bacfdf3a8c7b45b53', 'public_url': None}], 'next_cursor': None, 'has_more': False, 'type': 'page_or_database', 'page_or_database': {}, 'request_id': '44a57992-dbe9-4829-b67b-92c4fb645ccb'}
        self.people_result = {
            'object': 'list', 
            'results': [{'object': 'page', 'id': '1f0212ab-8856-8086-9216-e2fd27451d32', 'created_time': '2025-05-11T22:42:00.000Z', 'last_edited_time': '2025-05-11T22:42:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1ed212ab-8856-800c-af60-d3aea6b255d9'}, 'archived': False, 'in_trash': False, 'properties': {'Team': {'id': 'w%7BcP', 'type': 'relation', 'relation': [{'id': '1f0212ab-8856-803c-af2b-f19064ed2fc3'}], 'has_more': False}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'CJ', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'CJ', 'href': None}]}}, 'url': 'https://www.notion.so/CJ-1f0212ab885680869216e2fd27451d32', 'public_url': None}, {'object': 'page', 'id': '1f0212ab-8856-801b-bae3-e8a1ad3c4d2b', 'created_time': '2025-05-11T22:41:00.000Z', 'last_edited_time': '2025-05-11T22:42:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1ed212ab-8856-800c-af60-d3aea6b255d9'}, 'archived': False, 'in_trash': False, 'properties': {'Team': {'id': 'w%7BcP', 'type': 'relation', 'relation': [{'id': '1f0212ab-8856-803c-af2b-f19064ed2fc3'}], 'has_more': False}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Christine', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Christine', 'href': None}]}}, 'url': 'https://www.notion.so/Christine-1f0212ab8856801bbae3e8a1ad3c4d2b', 'public_url': None}, {'object': 'page', 'id': '1f0212ab-8856-8087-8b62-d409ebdf66a9', 'created_time': '2025-05-11T22:41:00.000Z', 'last_edited_time': '2025-05-11T22:42:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1ed212ab-8856-800c-af60-d3aea6b255d9'}, 'archived': False, 'in_trash': False, 'properties': {'Team': {'id': 'w%7BcP', 'type': 'relation', 'relation': [{'id': '1f0212ab-8856-803c-af2b-f19064ed2fc3'}], 'has_more': False}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Craig', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Craig', 'href': None}]}}, 'url': 'https://www.notion.so/Craig-1f0212ab885680878b62d409ebdf66a9', 'public_url': None}, {'object': 'page', 'id': '1f0212ab-8856-809d-bc03-ddc1082c59fa', 'created_time': '2025-05-11T22:41:00.000Z', 'last_edited_time': '2025-05-11T22:42:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1ed212ab-8856-800c-af60-d3aea6b255d9'}, 'archived': False, 'in_trash': False, 'properties': {'Team': {'id': 'w%7BcP', 'type': 'relation', 'relation': [{'id': '1f0212ab-8856-803c-af2b-f19064ed2fc3'}], 'has_more': False}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'JJ', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'JJ', 'href': None}]}}, 'url': 'https://www.notion.so/JJ-1f0212ab8856809dbc03ddc1082c59fa', 'public_url': None}, {'object': 'page', 'id': '1f0212ab-8856-805e-8144-d055db0ed580', 'created_time': '2025-05-11T22:19:00.000Z', 'last_edited_time': '2025-05-11T22:20:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1ed212ab-8856-800c-af60-d3aea6b255d9'}, 'archived': False, 'in_trash': False, 'properties': {'Team': {'id': 'w%7BcP', 'type': 'relation', 'relation': [{'id': '1f0212ab-8856-807b-acfd-f3a8c7b45b53'}], 'has_more': False}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Daisy', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Daisy', 'href': None}]}}, 'url': 'https://www.notion.so/Daisy-1f0212ab8856805e8144d055db0ed580', 'public_url': None}, {'object': 'page', 'id': '1f0212ab-8856-803c-93ee-f82f67c5502f', 'created_time': '2025-05-11T22:19:00.000Z', 'last_edited_time': '2025-05-11T22:20:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1ed212ab-8856-800c-af60-d3aea6b255d9'}, 'archived': False, 'in_trash': False, 'properties': {'Team': {'id': 'w%7BcP', 'type': 'relation', 'relation': [{'id': '1f0212ab-8856-807b-acfd-f3a8c7b45b53'}], 'has_more': False}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Peach', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Peach', 'href': None}]}}, 'url': 'https://www.notion.so/Peach-1f0212ab8856803c93eef82f67c5502f', 'public_url': None}, {'object': 'page', 'id': '1f0212ab-8856-800d-978e-dae17833c9a2', 'created_time': '2025-05-11T22:19:00.000Z', 'last_edited_time': '2025-05-11T22:19:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1ed212ab-8856-800c-af60-d3aea6b255d9'}, 'archived': False, 'in_trash': False, 'properties': {'Team': {'id': 'w%7BcP', 'type': 'relation', 'relation': [{'id': '1f0212ab-8856-807b-acfd-f3a8c7b45b53'}], 'has_more': False}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Luigi', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Luigi', 'href': None}]}}, 'url': 'https://www.notion.so/Luigi-1f0212ab8856800d978edae17833c9a2', 'public_url': None}, {'object': 'page', 'id': '1f0212ab-8856-809f-a6ec-e6a9b5a9ca0e', 'created_time': '2025-05-11T22:19:00.000Z', 'last_edited_time': '2025-05-11T22:19:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1ed212ab-8856-800c-af60-d3aea6b255d9'}, 'archived': False, 'in_trash': False, 'properties': {'Team': {'id': 'w%7BcP', 'type': 'relation', 'relation': [{'id': '1f0212ab-8856-807b-acfd-f3a8c7b45b53'}], 'has_more': False}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Mario', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Mario', 'href': None}]}}, 'url': 'https://www.notion.so/Mario-1f0212ab8856809fa6ece6a9b5a9ca0e', 'public_url': None}], 'next_cursor': None, 'has_more': False, 'type': 'page_or_database', 'page_or_database': {}, 'request_id': '8708d7c0-1f6d-40cc-a62d-c250c0163aed'}
        self.question_result = {'object': 'list', 
                   'results': 
                   [{
                       'object': 'page', 
                       'id': '1e6212ab-8856-80d7-8b65-cdb8c0a9028a', 
                       'created_time': '2025-05-01T03:46:00.000Z', 
                       'last_edited_time': '2025-05-03T16:53:00.000Z', 
                       'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 
                       'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 
                       'cover': None, 
                       'icon': None, 
                       'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 
                       'archived': False, 
                       'in_trash': False, 
                       'properties': 
                            {'Description': 
                             {'id': 'CPe%7B', 
                              'type': 'rich_text', 
                              'rich_text': []}, 
                            'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 
                            'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 30}, 
                            'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 
                            'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 
                            'Name': {'id': 'title', 
                                      'type': 'title', 
                                      'title': [{'type': 'text', 'text': {'content': 'What is the  furthest neighborhood from me?', 'link': None}, 
                                                                          'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 
                                                                          'plain_text': 'What is the  furthest neighborhood from me?', 'href': None}]
                                        }
                            }, 
                            'url': 'https://www.notion.so/What-is-the-furthest-neighborhood-from-me-1e6212ab885680d78b65cdb8c0a9028a', 
                            'public_url': 'https://jjs30th.notion.site/What-is-the-furthest-neighborhood-from-me-1e6212ab885680d78b65cdb8c0a9028a'}, 
                    {   'object': 'page', 
                        'id': '1e6212ab-8856-8014-b513-f5891c3e8c55', 
                        'created_time': '2025-05-01T03:46:00.000Z', 
                        'last_edited_time': '2025-05-03T16:53:00.000Z', 
                        'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 
                        'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 20}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Is the neighborhood agreed upon by >80% of the people based in NYT', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Is the neighborhood agreed upon by >80% of the people based in NYT', 'href': None}]}}, 'url': 'https://www.notion.so/Is-the-neighborhood-agreed-upon-by-80-of-the-people-based-in-NYT-1e6212ab88568014b513f5891c3e8c55', 'public_url': 'https://jjs30th.notion.site/Is-the-neighborhood-agreed-upon-by-80-of-the-people-based-in-NYT-1e6212ab88568014b513f5891c3e8c55'}, 
                        {'object': 'page', 'id': '1e6212ab-8856-8011-98d8-e20c3bee437b', 'created_time': '2025-05-01T03:46:00.000Z', 'last_edited_time': '2025-05-03T16:52:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 40}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'What types of employees work there?', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'What types of employees work there?', 'href': None}]}}, 'url': 'https://www.notion.so/What-types-of-employees-work-there-1e6212ab8856801198d8e20c3bee437b', 'public_url': 'https://jjs30th.notion.site/What-types-of-employees-work-there-1e6212ab8856801198d8e20c3bee437b'}, 
                        {'object': 'page', 'id': '1e6212ab-8856-8072-bd4a-d4c446a6aaa0', 'created_time': '2025-05-01T03:46:00.000Z', 'last_edited_time': '2025-05-03T16:52:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 20}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 
                        'select': {'id': 'de1da7b4-6218-427e-8f88-52d48b1d7f4e', 'name': 'About the Place', 'color': 'red'}}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'What’s the rating of this place?', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'What’s the rating of this place?', 'href': None}]}}, 'url': 'https://www.notion.so/What-s-the-rating-of-this-place-1e6212ab88568072bd4ad4c446a6aaa0', 'public_url': 'https://jjs30th.notion.site/What-s-the-rating-of-this-place-1e6212ab88568072bd4ad4c446a6aaa0'}, {'object': 'page', 'id': '1e6212ab-8856-8050-942f-decc3a933634', 'created_time': '2025-05-01T03:46:00.000Z', 'last_edited_time': '2025-05-03T16:52:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 20}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': {'id': 'de1da7b4-6218-427e-8f88-52d48b1d7f4e', 'name': 'About the Place', 'color': 'red'}}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Does this place have a wikipedia', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Does this place have a wikipedia', 'href': None}]}}, 'url': 'https://www.notion.so/Does-this-place-have-a-wikipedia-1e6212ab88568050942fdecc3a933634', 'public_url': 'https://jjs30th.notion.site/Does-this-place-have-a-wikipedia-1e6212ab88568050942fdecc3a933634'}, {'object': 'page', 'id': '1e6212ab-8856-80fa-8ce6-ceee6b7e7005', 'created_time': '2025-05-01T03:45:00.000Z', 'last_edited_time': '2025-05-03T16:52:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': 'N/A', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'N/A', 'href': None}]}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': None}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Sketch the storefront', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Sketch the storefront', 'href': None}]}}, 'url': 'https://www.notion.so/Sketch-the-storefront-1e6212ab885680fa8ce6ceee6b7e7005', 'public_url': 'https://jjs30th.notion.site/Sketch-the-storefront-1e6212ab885680fa8ce6ceee6b7e7005'}, {'object': 'page', 'id': '1e6212ab-8856-8013-a51b-f7cfb174f5ee', 'created_time': '2025-05-01T03:45:00.000Z', 'last_edited_time': '2025-05-03T16:52:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 60}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Take a photo of your nearest bagel shop/bodega dn remove teh words', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Take a photo of your nearest bagel shop/bodega dn remove teh words', 'href': None}]}}, 'url': 'https://www.notion.so/Take-a-photo-of-your-nearest-bagel-shop-bodega-dn-remove-teh-words-1e6212ab88568013a51bf7cfb174f5ee', 'public_url': 'https://jjs30th.notion.site/Take-a-photo-of-your-nearest-bagel-shop-bodega-dn-remove-teh-words-1e6212ab88568013a51bf7cfb174f5ee'}, {'object': 'page', 'id': '1e6212ab-8856-801b-baf2-efbc6bba426e', 'created_time': '2025-05-01T03:45:00.000Z', 'last_edited_time': '2025-05-03T16:51:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 10}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'What sports are played in the park', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'What sports are played in the park', 'href': None}]}}, 'url': 'https://www.notion.so/What-sports-are-played-in-the-park-1e6212ab8856801bbaf2efbc6bba426e', 'public_url': 'https://jjs30th.notion.site/What-sports-are-played-in-the-park-1e6212ab8856801bbaf2efbc6bba426e'}, {'object': 'page', 'id': '1e6212ab-8856-8099-84fc-d815608b7c50', 'created_time': '2025-05-01T03:44:00.000Z', 'last_edited_time': '2025-05-03T16:49:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 10}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Write a word that contains all the train line at your nearest station', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Write a word that contains all the train line at your nearest station', 'href': None}]}}, 'url': 'https://www.notion.so/Write-a-word-that-contains-all-the-train-line-at-your-nearest-station-1e6212ab8856809984fcd815608b7c50', 'public_url': 'https://jjs30th.notion.site/Write-a-word-that-contains-all-the-train-line-at-your-nearest-station-1e6212ab8856809984fcd815608b7c50'}, {'object': 'page', 'id': '1e6212ab-8856-80ac-83ad-e9eef5caf3e0', 'created_time': '2025-05-01T03:44:00.000Z', 'last_edited_time': '2025-05-03T16:49:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 20}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Name the closest 3 grocery stores', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Name the closest 3 grocery stores', 'href': None}]}}, 'url': 'https://www.notion.so/Name-the-closest-3-grocery-stores-1e6212ab885680ac83ade9eef5caf3e0', 'public_url': 'https://jjs30th.notion.site/Name-the-closest-3-grocery-stores-1e6212ab885680ac83ade9eef5caf3e0'}, {'object': 'page', 'id': '1e6212ab-8856-80f9-b59a-e24aa7ab5c69', 'created_time': '2025-05-01T03:44:00.000Z', 'last_edited_time': '2025-05-03T16:41:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 20}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'What buildings >100ft are in 200ft of me', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'What buildings >100ft are in 200ft of me', 'href': None}]}}, 'url': 'https://www.notion.so/What-buildings-100ft-are-in-200ft-of-me-1e6212ab885680f9b59ae24aa7ab5c69', 'public_url': 'https://jjs30th.notion.site/What-buildings-100ft-are-in-200ft-of-me-1e6212ab885680f9b59ae24aa7ab5c69'}, {'object': 'page', 'id': '1e6212ab-8856-808e-b55e-e54f938f23cd', 'created_time': '2025-05-01T03:44:00.000Z', 'last_edited_time': '2025-05-03T16:34:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 20}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Take a photo of dirt/lampost/trashcan', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Take a photo of dirt/lampost/trashcan', 'href': None}]}}, 'url': 'https://www.notion.so/Take-a-photo-of-dirt-lampost-trashcan-1e6212ab8856808eb55ee54f938f23cd', 'public_url': 'https://jjs30th.notion.site/Take-a-photo-of-dirt-lampost-trashcan-1e6212ab8856808eb55ee54f938f23cd'}, {'object': 'page', 'id': '1e6212ab-8856-8035-a583-c1b76626ca66', 'created_time': '2025-05-01T03:29:00.000Z', 'last_edited_time': '2025-05-03T16:34:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': 'N/A', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'N/A', 'href': None}]}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': None}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Something about schools and numbers', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Something about schools and numbers', 'href': None}]}}, 'url': 'https://www.notion.so/Something-about-schools-and-numbers-1e6212ab88568035a583c1b76626ca66', 'public_url': 'https://jjs30th.notion.site/Something-about-schools-and-numbers-1e6212ab88568035a583c1b76626ca66'}, {'object': 'page', 'id': '1e6212ab-8856-805b-af12-f4f4353312e3', 'created_time': '2025-05-01T03:29:00.000Z', 'last_edited_time': '2025-05-03T16:34:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': 'N/A', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'N/A', 'href': None}]}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': None}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'If I sum up all the buses in the neares bus stop, what is the sum of all the buses', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'If I sum up all the buses in the neares bus stop, what is the sum of all the buses', 'href': None}]}}, 'url': 'https://www.notion.so/If-I-sum-up-all-the-buses-in-the-neares-bus-stop-what-is-the-sum-of-all-the-buses-1e6212ab8856805baf12f4f4353312e3', 'public_url': 'https://jjs30th.notion.site/If-I-sum-up-all-the-buses-in-the-neares-bus-stop-what-is-the-sum-of-all-the-buses-1e6212ab8856805baf12f4f4353312e3'}, {'object': 'page', 'id': '1e6212ab-8856-80ba-bf18-c2059d7716b2', 'created_time': '2025-05-01T03:28:00.000Z', 'last_edited_time': '2025-05-03T16:34:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': 'Choose a direction .5 miles and I’ll tell you if you’re hot or cold', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Choose a direction .5 miles and I’ll tell you if you’re hot or cold', 'href': None}]}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 40}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Hot or cold', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Hot or cold', 'href': None}]}}, 'url': 'https://www.notion.so/Hot-or-cold-1e6212ab885680babf18c2059d7716b2', 'public_url': 'https://jjs30th.notion.site/Hot-or-cold-1e6212ab885680babf18c2059d7716b2'}, {'object': 'page', 'id': '1e6212ab-8856-80dd-8950-d8accb4996ed', 'created_time': '2025-05-01T03:28:00.000Z', 'last_edited_time': '2025-05-03T16:33:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 50}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'What type of building am I in?', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'What type of building am I in?', 'href': None}]}}, 'url': 'https://www.notion.so/What-type-of-building-am-I-in-1e6212ab885680dd8950d8accb4996ed', 'public_url': 'https://jjs30th.notion.site/What-type-of-building-am-I-in-1e6212ab885680dd8950d8accb4996ed'}, {'object': 'page', 'id': '1e6212ab-8856-8035-a344-e2eee065fbdb', 'created_time': '2025-05-01T03:28:00.000Z', 'last_edited_time': '2025-05-03T16:33:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 40}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'What’s the last food I saw', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'What’s the last food I saw', 'href': None}]}}, 'url': 'https://www.notion.so/What-s-the-last-food-I-saw-1e6212ab88568035a344e2eee065fbdb', 'public_url': 'https://jjs30th.notion.site/What-s-the-last-food-I-saw-1e6212ab88568035a344e2eee065fbdb'}, {'object': 'page', 'id': '1e6212ab-8856-80fd-a832-d1d8caaf97fe', 'created_time': '2025-05-01T03:26:00.000Z', 'last_edited_time': '2025-05-03T16:30:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 60}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'What is your compass degree from the Brooklyn Tower', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'What is your compass degree from the Brooklyn Tower', 'href': None}]}}, 'url': 'https://www.notion.so/What-is-your-compass-degree-from-the-Brooklyn-Tower-1e6212ab885680fda832d1d8caaf97fe', 'public_url': 'https://jjs30th.notion.site/What-is-your-compass-degree-from-the-Brooklyn-Tower-1e6212ab885680fda832d1d8caaf97fe'}, {'object': 'page', 'id': '1e6212ab-8856-8021-a40f-d118d86d8cd6', 'created_time': '2025-05-01T01:51:00.000Z', 'last_edited_time': '2025-05-03T16:30:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 100}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'What’s the nearest neighborhood library', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'What’s the nearest neighborhood library', 'href': None}]}}, 'url': 'https://www.notion.so/What-s-the-nearest-neighborhood-library-1e6212ab88568021a40fd118d86d8cd6', 'public_url': 'https://jjs30th.notion.site/What-s-the-nearest-neighborhood-library-1e6212ab88568021a40fd118d86d8cd6'}, {'object': 'page', 'id': '1e6212ab-8856-80f0-885c-fbc78a9ccb45', 'created_time': '2025-05-01T01:50:00.000Z', 'last_edited_time': '2025-05-03T16:30:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 10}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Send me a song that gives me the vibe of your neighborhood', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Send me a song that gives me the vibe of your neighborhood', 'href': None}]}}, 'url': 'https://www.notion.so/Send-me-a-song-that-gives-me-the-vibe-of-your-neighborhood-1e6212ab885680f0885cfbc78a9ccb45', 'public_url': 'https://jjs30th.notion.site/Send-me-a-song-that-gives-me-the-vibe-of-your-neighborhood-1e6212ab885680f0885cfbc78a9ccb45'}, {'object': 'page', 'id': '1e6212ab-8856-803d-8536-c6dbef31c8c3', 'created_time': '2025-05-01T01:33:00.000Z', 'last_edited_time': '2025-05-03T16:30:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 30}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Is your neighborhood in empire state of mind', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Is your neighborhood in empire state of mind', 'href': None}]}}, 'url': 'https://www.notion.so/Is-your-neighborhood-in-empire-state-of-mind-1e6212ab8856803d8536c6dbef31c8c3', 'public_url': 'https://jjs30th.notion.site/Is-your-neighborhood-in-empire-state-of-mind-1e6212ab8856803d8536c6dbef31c8c3'}, {'object': 'page', 'id': '1e6212ab-8856-80df-85c4-fc82899bfa80', 'created_time': '2025-05-01T01:33:00.000Z', 'last_edited_time': '2025-05-03T16:30:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 40}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Are you in X neighborhood', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Are you in X neighborhood', 'href': None}]}}, 'url': 'https://www.notion.so/Are-you-in-X-neighborhood-1e6212ab885680df85c4fc82899bfa80', 'public_url': 'https://jjs30th.notion.site/Are-you-in-X-neighborhood-1e6212ab885680df85c4fc82899bfa80'}, {'object': 'page', 'id': '1e6212ab-8856-803d-ac75-fbbcd7d3c58e', 'created_time': '2025-05-01T01:28:00.000Z', 'last_edited_time': '2025-05-03T16:30:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 40}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Am I in the same neighborhood', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Am I in the same neighborhood', 'href': None}]}}, 'url': 'https://www.notion.so/Am-I-in-the-same-neighborhood-1e6212ab8856803dac75fbbcd7d3c58e', 'public_url': 'https://jjs30th.notion.site/Am-I-in-the-same-neighborhood-1e6212ab8856803dac75fbbcd7d3c58e'}, {'object': 'page', 'id': '1e6212ab-8856-8084-91a3-d5f6f705af67', 'created_time': '2025-05-01T01:26:00.000Z', 'last_edited_time': '2025-05-03T16:30:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 40}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'How many neighborhoods does your neighborhood neighbor', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'How many neighborhoods does your neighborhood neighbor', 'href': None}]}}, 'url': 'https://www.notion.so/How-many-neighborhoods-does-your-neighborhood-neighbor-1e6212ab8856808491a3d5f6f705af67', 'public_url': 'https://jjs30th.notion.site/How-many-neighborhoods-does-your-neighborhood-neighbor-1e6212ab8856808491a3d5f6f705af67'}, {'object': 'page', 'id': '1e6212ab-8856-8064-b68a-c7a1c2ec3832', 'created_time': '2025-05-01T01:26:00.000Z', 'last_edited_time': '2025-05-03T16:30:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 20}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'How many people are in the same room as you?', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'How many people are in the same room as you?', 'href': None}]}}, 'url': 'https://www.notion.so/How-many-people-are-in-the-same-room-as-you-1e6212ab88568064b68ac7a1c2ec3832', 'public_url': 'https://jjs30th.notion.site/How-many-people-are-in-the-same-room-as-you-1e6212ab88568064b68ac7a1c2ec3832'}, {'object': 'page', 'id': '1e6212ab-8856-8044-bb77-c8523549a727', 'created_time': '2025-05-01T01:26:00.000Z', 'last_edited_time': '2025-05-03T16:29:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 30}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'How many stoires are in my building', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'How many stoires are in my building', 'href': None}]}}, 'url': 'https://www.notion.so/How-many-stoires-are-in-my-building-1e6212ab88568044bb77c8523549a727', 'public_url': 'https://jjs30th.notion.site/How-many-stoires-are-in-my-building-1e6212ab88568044bb77c8523549a727'}, {'object': 'page', 'id': '1e6212ab-8856-80ce-960d-ebcf20d479fb', 'created_time': '2025-05-01T01:26:00.000Z', 'last_edited_time': '2025-05-03T16:29:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 20}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Send outline of the block', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Send outline of the block', 'href': None}]}}, 'url': 'https://www.notion.so/Send-outline-of-the-block-1e6212ab885680ce960debcf20d479fb', 'public_url': 'https://jjs30th.notion.site/Send-outline-of-the-block-1e6212ab885680ce960debcf20d479fb'}, {'object': 'page', 'id': '1e6212ab-8856-8088-8e2d-f5082fe8cc96', 'created_time': '2025-05-01T01:26:00.000Z', 'last_edited_time': '2025-05-03T16:29:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 10}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': {'id': 'ff460acc-981a-4bfc-81b2-cad6ac0452b1', 'name': 'Photo', 'color': 'purple'}}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Send an audio recording of the spot', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Send an audio recording of the spot', 'href': None}]}}, 'url': 'https://www.notion.so/Send-an-audio-recording-of-the-spot-1e6212ab885680888e2df5082fe8cc96', 'public_url': 'https://jjs30th.notion.site/Send-an-audio-recording-of-the-spot-1e6212ab885680888e2df5082fe8cc96'}, {'object': 'page', 'id': '1e5212ab-8856-801e-b442-f1ae91e3bec4', 'created_time': '2025-04-30T12:21:00.000Z', 'last_edited_time': '2025-05-03T16:29:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 20}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Give me a 1 letter/digit of st', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Give me a 1 letter/digit of st', 'href': None}]}}, 'url': 'https://www.notion.so/Give-me-a-1-letter-digit-of-st-1e5212ab8856801eb442f1ae91e3bec4', 'public_url': 'https://jjs30th.notion.site/Give-me-a-1-letter-digit-of-st-1e5212ab8856801eb442f1ae91e3bec4'}, {'object': 'page', 'id': '1e5212ab-8856-80c2-ba30-efcee0a9ac0e', 'created_time': '2025-04-30T12:20:00.000Z', 'last_edited_time': '2025-05-03T16:29:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 40}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'How many  bikes are at the closest citibike station', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'How many  bikes are at the closest citibike station', 'href': None}]}}, 'url': 'https://www.notion.so/How-many-bikes-are-at-the-closest-citibike-station-1e5212ab885680c2ba30efcee0a9ac0e', 'public_url': 'https://jjs30th.notion.site/How-many-bikes-are-at-the-closest-citibike-station-1e5212ab885680c2ba30efcee0a9ac0e'}, {'object': 'page', 'id': '1e5212ab-8856-80e4-a744-ebd9b739a29b', 'created_time': '2025-04-30T12:20:00.000Z', 'last_edited_time': '2025-05-03T16:24:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 150}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Closest Citibike location', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Closest Citibike location', 'href': None}]}}, 'url': 'https://www.notion.so/Closest-Citibike-location-1e5212ab885680e4a744ebd9b739a29b', 'public_url': 'https://jjs30th.notion.site/Closest-Citibike-location-1e5212ab885680e4a744ebd9b739a29b'}, {'object': 'page', 'id': '1e5212ab-8856-805e-b723-e749e3105bf4', 'created_time': '2025-04-30T12:17:00.000Z', 'last_edited_time': '2025-05-03T21:00:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': 'https://support.garmin.com/en-US/?faq=hRMBoCTy5a7HqVkxukhHd8', 'link': {'url': 'https://support.garmin.com/en-US/?faq=hRMBoCTy5a7HqVkxukhHd8'}}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'https://support.garmin.com/en-US/?faq=hRMBoCTy5a7HqVkxukhHd8', 'href': 'https://support.garmin.com/en-US/?faq=hRMBoCTy5a7HqVkxukhHd8'}]}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 100}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'General Longitude and Latitude', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'General Longitude and Latitude', 'href': None}]}}, 'url': 'https://www.notion.so/General-Longitude-and-Latitude-1e5212ab8856805eb723e749e3105bf4', 'public_url': 'https://jjs30th.notion.site/General-Longitude-and-Latitude-1e5212ab8856805eb723e749e3105bf4'}, {'object': 'page', 'id': '1e5212ab-8856-80a0-9762-e2ced1c4621b', 'created_time': '2025-04-30T12:15:00.000Z', 'last_edited_time': '2025-05-03T16:24:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 20}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': {'id': 'ff460acc-981a-4bfc-81b2-cad6ac0452b1', 'name': 'Photo', 'color': 'purple'}}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Selfie', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Selfie', 'href': None}]}}, 'url': 'https://www.notion.so/Selfie-1e5212ab885680a09762e2ced1c4621b', 'public_url': 'https://jjs30th.notion.site/Selfie-1e5212ab885680a09762e2ced1c4621b'}, {'object': 'page', 'id': '1e5212ab-8856-8035-bac3-da9170ed3a45', 'created_time': '2025-04-30T12:14:00.000Z', 'last_edited_time': '2025-05-03T16:24:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 40}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': {'id': 'ff460acc-981a-4bfc-81b2-cad6ac0452b1', 'name': 'Photo', 'color': 'purple'}}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Photo of the sidewalk', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Photo of the sidewalk', 'href': None}]}}, 'url': 'https://www.notion.so/Photo-of-the-sidewalk-1e5212ab88568035bac3da9170ed3a45', 'public_url': 'https://jjs30th.notion.site/Photo-of-the-sidewalk-1e5212ab88568035bac3da9170ed3a45'}, {'object': 'page', 'id': '1e5212ab-8856-80fe-9aac-c0bc2e95d848', 'created_time': '2025-04-30T12:14:00.000Z', 'last_edited_time': '2025-05-03T16:24:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 20}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': {'id': 'ff460acc-981a-4bfc-81b2-cad6ac0452b1', 'name': 'Photo', 'color': 'purple'}}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Photo of whatever is above me', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Photo of whatever is above me', 'href': None}]}}, 'url': 'https://www.notion.so/Photo-of-whatever-is-above-me-1e5212ab885680fe9aacc0bc2e95d848', 'public_url': 'https://jjs30th.notion.site/Photo-of-whatever-is-above-me-1e5212ab885680fe9aacc0bc2e95d848'}, {'object': 'page', 'id': '1e5212ab-8856-8024-bdbc-d9b7f5d2a27a', 'created_time': '2025-04-30T12:14:00.000Z', 'last_edited_time': '2025-05-03T16:24:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 20}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Give me the average rent of your neighborhood', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Give me the average rent of your neighborhood', 'href': None}]}}, 'url': 'https://www.notion.so/Give-me-the-average-rent-of-your-neighborhood-1e5212ab88568024bdbcd9b7f5d2a27a', 'public_url': 'https://jjs30th.notion.site/Give-me-the-average-rent-of-your-neighborhood-1e5212ab88568024bdbcd9b7f5d2a27a'}, {'object': 'page', 'id': '1e5212ab-8856-80d8-a05d-fef123a371d5', 'created_time': '2025-04-30T12:08:00.000Z', 'last_edited_time': '2025-05-03T16:24:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 5}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Give me a fun fact', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Give me a fun fact', 'href': None}]}}, 'url': 'https://www.notion.so/Give-me-a-fun-fact-1e5212ab885680d8a05dfef123a371d5', 'public_url': 'https://jjs30th.notion.site/Give-me-a-fun-fact-1e5212ab885680d8a05dfef123a371d5'}, {'object': 'page', 'id': '1e5212ab-8856-803e-bd26-caf011ae625d', 'created_time': '2025-04-30T12:08:00.000Z', 'last_edited_time': '2025-05-03T16:23:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 40}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'How many [Chain stores] are within 1 mile of me', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'How many [Chain stores] are within 1 mile of me', 'href': None}]}}, 'url': 'https://www.notion.so/How-many-Chain-stores-are-within-1-mile-of-me-1e5212ab8856803ebd26caf011ae625d', 'public_url': 'https://jjs30th.notion.site/How-many-Chain-stores-are-within-1-mile-of-me-1e5212ab8856803ebd26caf011ae625d'}, {'object': 'page', 'id': '1e5212ab-8856-801f-9533-d35ad9070f14', 'created_time': '2025-04-30T12:08:00.000Z', 'last_edited_time': '2025-05-03T16:05:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': []}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 40}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Am I within X miles', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Am I within X miles', 'href': None}]}}, 'url': 'https://www.notion.so/Am-I-within-X-miles-1e5212ab8856801f9533d35ad9070f14', 'public_url': 'https://jjs30th.notion.site/Am-I-within-X-miles-1e5212ab8856801f9533d35ad9070f14'}, {'object': 'page', 'id': '1e5212ab-8856-80f3-a3bd-c8bda6d9cefe', 'created_time': '2025-04-30T12:07:00.000Z', 'last_edited_time': '2025-05-03T15:20:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1e5212ab-8856-802c-a014-d865b47bb655'}, 'archived': False, 'in_trash': False, 'properties': {'Description': {'id': 'CPe%7B', 'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': 'This will be presented in color, not in ', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'This will be presented in color, not in ', 'href': None}]}, 'Additional Info': {'id': 'PioV', 'type': 'select', 'select': None}, 'Cost': {'id': 'XXL%5B', 'type': 'number', 'number': 50}, 'Team Asked Question': {'id': 'iJiV', 'type': 'relation', 'relation': [], 'has_more': False}, 'Category': {'id': 'yA%5E%7B', 'type': 'select', 'select': None}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Closest Metro Line', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Closest Metro Line', 'href': None}]}}, 'url': 'https://www.notion.so/Closest-Metro-Line-1e5212ab885680f3a3bdc8bda6d9cefe', 'public_url': 'https://jjs30th.notion.site/Closest-Metro-Line-1e5212ab885680f3a3bdc8bda6d9cefe'}], 'next_cursor': None, 'has_more': False, 'type': 'page_or_database', 'page_or_database': {}, 'request_id': 'ae0b6593-cea1-4954-80cd-19c2dbf9d578'}
        self.card_result = {'object': 
          'list', 
          'results': 
            [{'object': 'page', 
                'id': '1f0212ab-8856-80e6-905f-da800fad1b3b', 
                'created_time': '2025-05-11T14:55:00.000Z', 
                'last_edited_time': '2025-05-11T14:55:00.000Z', 
                'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 
                'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 
                'cover': None, 
                'icon': None, 
                'parent': {'type': 'database_id', 'database_id': '1ed212ab-8856-8070-babe-ea276dad7af3'}, 
                'archived': False, 
                'in_trash': False, 
                'properties': 
                    {'Team Favorite Card': {'id': '%3EN%3Bd', 'type': 'relation', 'relation': [], 'has_more': False}, 
                     'Description': {'id': '%3EO%40T', 
                                     'type': 'rich_text', 
                                     'rich_text': [{'type': 'text', 
                                                    'text': {'content': 'What a special card!', 'link': None}, 
                                                    'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 
                                                    'plain_text': 'What a special card!', 'href': None}]
                                    }, 
                     'Team Completed Cards': {'id': 'Xrre', 'type': 'relation', 'relation': [], 'has_more': False}, 
                     'Points': {'id': '%7DpxD', 'type': 'number', 'number': 500}, 
                     'Name': {'id': 'title', 'type': 'title', 
                              'title': [
                                  {'type': 'text', 
                                   'text': {'content': 'Special card', 'link': None}, 
                                   'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 
                                   'plain_text': 'Special card', 'href': None}]
                              }
                    }, 'url': 'https://www.notion.so/Special-card-1f0212ab885680e6905fda800fad1b3b', 'public_url': None}, {'object': 'page', 'id': '1f0212ab-8856-80f2-8160-e650f5ab409a', 'created_time': '2025-05-11T14:55:00.000Z', 'last_edited_time': '2025-05-11T14:55:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1ed212ab-8856-8070-babe-ea276dad7af3'}, 'archived': False, 'in_trash': False, 'properties': {'Team Favorite Card': {'id': '%3EN%3Bd', 'type': 'relation', 'relation': [], 'has_more': False}, 'Description': {'id': '%3EO%40T', 'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': 'Description of Goodbye world', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Description of Goodbye world', 'href': None}]}, 'Team Completed Cards': {'id': 'Xrre', 'type': 'relation', 'relation': [], 'has_more': False}, 'Points': {'id': '%7DpxD', 'type': 'number', 'number': 90}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Goodbye world!', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Goodbye world!', 'href': None}]}}, 'url': 'https://www.notion.so/Goodbye-world-1f0212ab885680f28160e650f5ab409a', 'public_url': None}, {'object': 'page', 'id': '1f0212ab-8856-80c4-8590-dd06d0a4cd60', 'created_time': '2025-05-11T14:46:00.000Z', 'last_edited_time': '2025-05-11T14:55:00.000Z', 'created_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'last_edited_by': {'object': 'user', 'id': '969024ab-610b-48f6-802f-c96f18d94181'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '1ed212ab-8856-8070-babe-ea276dad7af3'}, 'archived': False, 'in_trash': False, 'properties': {'Team Favorite Card': {'id': '%3EN%3Bd', 'type': 'relation', 'relation': [], 'has_more': False}, 'Description': {'id': '%3EO%40T', 'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': 'Description of Hello world', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Description of Hello world', 'href': None}]}, 'Team Completed Cards': {'id': 'Xrre', 'type': 'relation', 'relation': [], 'has_more': False}, 'Points': {'id': '%7DpxD', 'type': 'number', 'number': 30}, 'Name': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': 'Hello world!', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'Hello world!', 'href': None}]}}, 'url': 'https://www.notion.so/Hello-world-1f0212ab885680c48590dd06d0a4cd60', 'public_url': None}], 'next_cursor': None, 'has_more': False, 'type': 'page_or_database', 'page_or_database': {}, 'request_id': '299c99b2-282a-4b6b-9e14-3db943752118'}
        self.timeline_result = {
    "object": "list",
    "results": [
        {
            "object": "page",
            "id": "1f4212ab-8856-80e9-b0f7-ea185443ae2d",
            "created_time": "2025-05-15T22:31:00.000Z",
            "last_edited_time": "2025-05-15T22:31:00.000Z",
            "created_by": {
                "object": "user",
                "id": "969024ab-610b-48f6-802f-c96f18d94181"
            },
            "last_edited_by": {
                "object": "user",
                "id": "969024ab-610b-48f6-802f-c96f18d94181"
            },
            "cover": None,
            "icon": None,
            "parent": {
                "type": "database_id",
                "database_id": "1f4212ab-8856-8070-a0ed-de8d9ce3b437"
            },
            "archived": False,
            "in_trash": False,
            "properties": {
                "Asked Question": {
                    "id": "LkHQ",
                    "type": "relation",
                    "relation": [
                        {
                            "id": "1e5212ab-8856-80e4-a744-ebd9b739a29b"
                        }
                    ],
                    "has_more": False
                },
                "Completed Card": {
                    "id": "e~gH",
                    "type": "relation",
                    "relation": [],
                    "has_more": False
                },
                "Additional Points": {
                    "id": "tUux",
                    "type": "number",
                    "number": None
                },
                "Teams": {
                    "id": "zagu",
                    "type": "relation",
                    "relation": [
                        {
                            "id": "1f0212ab-8856-807b-acfd-f3a8c7b45b53"
                        }
                    ],
                    "has_more": False
                },
                "Name": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Lost something",
                                "link": None
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": "Lost something",
                            "href": None
                        }
                    ]
                }
            },
            "url": "https://www.notion.so/Lost-something-1f4212ab885680e9b0f7ea185443ae2d",
            "public_url": None
        },
        {
            "object": "page",
            "id": "1f4212ab-8856-802b-86df-d288d7d55b3d",
            "created_time": "2025-05-15T22:30:00.000Z",
            "last_edited_time": "2025-05-15T22:31:00.000Z",
            "created_by": {
                "object": "user",
                "id": "969024ab-610b-48f6-802f-c96f18d94181"
            },
            "last_edited_by": {
                "object": "user",
                "id": "969024ab-610b-48f6-802f-c96f18d94181"
            },
            "cover": None,
            "icon": None,
            "parent": {
                "type": "database_id",
                "database_id": "1f4212ab-8856-8070-a0ed-de8d9ce3b437"
            },
            "archived": False,
            "in_trash": False,
            "properties": {
                "Asked Question": {
                    "id": "LkHQ",
                    "type": "relation",
                    "relation": [],
                    "has_more": False
                },
                "Completed Card": {
                    "id": "e~gH",
                    "type": "relation",
                    "relation": [],
                    "has_more": False
                },
                "Additional Points": {
                    "id": "tUux",
                    "type": "number",
                    "number": 200
                },
                "Teams": {
                    "id": "zagu",
                    "type": "relation",
                    "relation": [
                        {
                            "id": "1f0212ab-8856-807b-acfd-f3a8c7b45b53"
                        }
                    ],
                    "has_more": False
                },
                "Name": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Base points",
                                "link": None
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": "Base points",
                            "href": None
                        }
                    ]
                }
            },
            "url": "https://www.notion.so/Base-points-1f4212ab8856802b86dfd288d7d55b3d",
            "public_url": None
        }
    ],
    "next_cursor": None,
    "has_more": False,
    "type": "page_or_database",
    "page_or_database": {},
    "developer_survey": "https://notionup.typeform.com/to/bllBsoI4?utm_source=postman",
    "request_id": "faca8cf6-b180-4fcc-abc1-e3ff6f2b92d3"
}
        self.leaderboard = lb.Leaderboard([], [])
        prq = LifoQueue()
        crq = LifoQueue()
        qrq = LifoQueue()
        trq = LifoQueue()
        tlq = LifoQueue()
        t1 = th.Thread(target=self.fetch_online_results, args = (prq, crq, qrq, trq, tlq), daemon=True)
        t2 = th.Thread(target=self.store_results, args = (prq, crq, qrq, trq, tlq), daemon=True)
        t1.start()
        t2.start()


    def get_player(self, id: str) -> sc.Player:
        for a_player in self.people_result['results']:
            player = self.player_parser(a_player)
            if player.id == id:
                return player
        return None

    def get_all_players(self) -> list[sc.Player]:
        return self.play_rel_to_list(self.people_result['results'])

    def get_question(self, id: str) -> sc.Question:
        for a_question in self.question_result['results']:
            question = self.question_parser(a_question)
            if question.id == id:
                return question
        return None

    def get_all_questions(self) -> list[sc.Question]:
        return self.ques_rel_to_list(self.question_result['results'])

    def get_team(self, id: str) -> sc.Team:
        for a_team in self.team_result['results']:
            team = self.team_parser(a_team)
            if team.id == id:
                self.get_accurate_team_cards([team], self.get_all_cards())
                return team
        return None

    def get_all_teams(self) -> list[sc.Team]:
        teams = self.team_rel_to_list(self.team_result['results'])
        cards = self.get_all_cards()
        self.get_accurate_team_cards(teams, cards)
        return teams

    def get_card(self, id: str) -> sc.Card:
        for a_card in self.card_result['results']:
            card = self.card_parser(a_card)
            if card.id == id:
                return card
        return None

    def get_all_cards(self) -> list[sc.Card]:
        return self.card_rel_to_list(self.card_result['results'])
    
    def get_all_timelines(self) -> list[sc.Timeline]:
        return self.timeline_rel_to_list(self.timeline_result['results'])
 
    def card_parser(self, cr):
        prop = cr['properties']
        id = cr['id']
        if id is None:
            return sc.Card("Null", "Null Card", "Invalid Card", 0, [])
        title_try = prop['Name']['title']
        title = title_try[0]['plain_text'] if len(title_try) > 0 else ""
        desc = prop['Description']['rich_text'][0]['plain_text']
        points = prop['Points']['number']
        difficulty = ''
        if 'Difficulty' in prop:
            difficulty = prop['Difficulty']['select']
            if difficulty is not None:
                difficulty = difficulty['name']
        team_ids = []
        for result in prop['Team Completed Cards']['relation']:
            team_ids.append(result['id'])
        return sc.Card(id, title, desc, points, team_ids, difficulty)

    def card_rel_to_list(self, cards_object):
        cards = []
        for object in cards_object:
            card = self.get_card(object['id'])
            if card is not None:
                cards.append(card)
        return cards

    def question_parser(self, qr):
        prop = qr['properties']
        id = qr['id']
        if id is None:
            return sc.Question("Null", "In progress question", "Still in progress", 0, "Null", False)
        title_try = prop['Name']['title']
        title = title_try[0]['plain_text'] if len(title_try) > 0 else ""
        desc = ''
        if len(prop['Description']['rich_text']) > 0:
            desc = prop['Description']['rich_text'][0]['plain_text']
        cost = prop['Cost']['number']
        category = prop['Category']['select']
        if category is not None:
            category = category['name']
        else:
            category = ''
        addtl = prop['Additional Info']['select']
        if addtl is not None and addtl['name'] != 'False':
            addtl = True
        else:
            addtl = False
        return sc.Question(id, title, desc, cost, category, addtl)

    def ques_rel_to_list(self, questions_object):
        questions = []
        for object in questions_object:
            question = self.get_question(object['id'])
            if question is not None:
                questions.append(question)
        return questions

    def player_parser(self, pr) -> sc.Player:
        prop = pr['properties']
        id = pr['id']
        name = prop['Name']['title'][0]['plain_text']
        return sc.Player(id, name)        

    def play_rel_to_list(self, players_object):
        players = []
        for object in players_object:
            player = self.get_player(object['id'])
            if player is not None:
                players.append(player)
        return players
    
    def team_rel_to_list(self, teams_object):
        teams = []
        for object in teams_object:
            team = self.get_team(object['id'])
            if team is not None:
                teams.append(team)
        return teams

    def team_parser(self, tr):
        prop = tr['properties']
        id = tr['id']
        if id is None:
            return sc.Team("None", [], "Null Team", 0, [], [], [])
        title_try = prop['Name']['title']
        name = title_try[0]['plain_text'] if len(title_try) > 0 else ""
        key = ''
        if 'Key' in prop:
            if len(prop['Key']['rich_text']) > 0:
                key = prop['Key']['rich_text'][0]['plain_text']
        discord_id = 0
        if 'Discord Channel' in prop:
            prop['Discord Channel']['number']
        players_object = prop['Players']['relation']
        compl_cards_object = prop['Completed Cards']['relation']
        fav_cards_object = prop['Favorite Cards']['relation']
        ask_quest_object = prop['Asked Questions']['relation']
        points = prop['Points']['number']
        players = self.play_rel_to_list(players_object)
        compl_cards = self.card_rel_to_list(compl_cards_object)
        fav_cards = self.card_rel_to_list(fav_cards_object)
        ask_quest = self.ques_rel_to_list(ask_quest_object)
        return sc.Team(id, players, name, points, compl_cards, fav_cards, ask_quest, discord_id, key)
    
    def timeline_parser(self, tr):
        prop = tr['properties']
        id = tr['id']
        if id is None:
            return (sc.Timeline("None", "In progress", 0))
        title_try = prop['Name']['title']
        name = title_try[0]['plain_text'] if len(title_try) > 0 else ""
        additional_points = prop['Additional Points']['number']
        teams_relations = prop['Teams']['relation']
        ask_quest_object = prop['Asked Question']['relation']
        teams = self.team_rel_to_list(teams_relations)
        ask_quests = self.ques_rel_to_list(ask_quest_object)
        team = None
        ask_quest = None
        if len(teams) > 0:
            team = teams[0]
        if len(ask_quests) > 0:
            ask_quest = ask_quests[0]
        if additional_points is None:
            additional_points = 0
        
        return sc.Timeline(id, name, additional_points,  team, ask_quest)
    
    def get_timeline(self, id: str) -> sc.Team:
        for a_time in self.timeline_result['results']:
            the_time = self.timeline_parser(a_time)
            if the_time.id == id:
                return the_time
        return None

    def timeline_rel_to_list(self, timeline_object):
        timelines = []
        for object in timeline_object:
            times = self.get_timeline(object['id'])
            if times is not None:
                timelines.append(times)
        return timelines


    def fetch_online_results(self, prq: Queue, crq: Queue, qrq: Queue, trq: Queue, tlq: Queue):
        total_sleep_count = 3
        while True:
            up_pr = notion.databases.query("1ed212ab8856800caf60d3aea6b255d9")
            time.sleep(total_sleep_count)
            up_cr = notion.databases.query("1ed212ab88568070babeea276dad7af3")
            time.sleep(total_sleep_count)
            up_qr = notion.databases.query("1e5212ab8856802ca014d865b47bb655")
            time.sleep(total_sleep_count)
            up_tr = notion.databases.query("1ed212ab885680ec85eed3c8d79109c0")
            time.sleep(total_sleep_count)
            up_tl = notion.databases.query("1f4212ab88568070a0edde8d9ce3b437")
            trq.put(up_tr)
            prq.put(up_pr)
            qrq.put(up_qr)
            crq.put(up_cr)
            tlq.put(up_tl)
    
    def store_results(self, prq: Queue, crq: Queue, qrq: Queue, trq: Queue, tlq: Queue):
        while True:
            self.people_result = prq.get()
            self.card_result = crq.get()
            self.question_result = qrq.get()
            self.team_result = trq.get()
            self.timeline_result = tlq.get()
            self.update_points(self.get_all_timelines(), self.get_all_teams())
            time.sleep(1)
            print("------------New Print Cycle---------------")

    def get_accurate_team_cards(self, teams: list[sc.Team], cards: list[sc.Card]):
        for team in teams:
            team.get_accurate_completed(cards)
    
    def update_points(self, timeline: list[sc.Timeline], teams: list[sc.Team]):
        all_changes = self.leaderboard.calculate_points(timeline, teams)
        point_dif = all_changes[1]
        print(point_dif)
        for team_id, points in point_dif.items():
            properties = {
                'Points': points['new_points']
            }
            notion.pages.update(team_id, properties=properties)


    def favorite_question(self, team_id, card_id):
        print("We're at notion fetcher with the team and card ids")
        relations = notion.pages.properties.retrieve(team_id, "SI_B")
        ids = []
        for result in relations["results"]:
            ids.append({"id": result["relation"]["id"] })
        ids.append({"id": card_id})
        properties = {
            'Favorite Cards': {
                "relation": ids
            }
        }
        notion.pages.update(team_id, properties=properties)

    def unfavorite_question(self, team_id, card_id):
        relations = notion.pages.properties.retrieve(team_id, "SI_B")
        ids = []
        for result in relations["results"]:
            if (card_id != result["relation"]["id"]):
                ids.append({"id": result["relation"]["id"] })
        properties = {
            'Favorite Cards': {
                "relation": ids
            }
        }
        notion.pages.update(team_id, properties=properties)
