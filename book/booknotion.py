"""
Documents: https://www.python-engineer.com/posts/notion-api-python/
INTEGRATION: https://www.notion.so/my-integrations
DATABASE_ID: https://booknotion.site/setting-databaseid

exaample data_format
{
'📎  Media': {'id': 'IiHm', 'type': 'files', 'files': []}, 
'📙  Book Title': {'id': 'OVh%7B', 'type': 'select', 'select': {'id': '1cd38ed4-888e-46a4-bb55-4c9033c6a55f', 'name': '「超」メタ思考 頭がよくなる最強トレーニング57連発', 'color': 'blue'}}, 
'Created At': {'id': 'Zjhb', 'type': 'created_time', 'created_time': '2023-05-28T11:40:00.000Z'}, 
'🏷  Tags': {'id': '_gxu', 'type': 'multi_select', 'multi_select': []}, 
'💬  Comment': {'id': 'r%60N%40', 'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': '', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': '', 'href': None}]}, 
'✍🏼  Author': {'id': 'x%3CeX', 'type': 'select', 'select': {'id': 'e0c7fa2f-5ce7-458e-8d03-6d5ae12f367d', 'name': 'ハック大学 ぺそ', 'color': 'blue'}}, 
'📝  Highlight': {'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': '①課題の認識（何が問題で、最終的にどうしたいのかを正しく捉える） ②課題の推論（何をするのか、何から始めるのか、仮説を立てて整理する） ③施策の執行（決めたタスクを決めた手順で行う）', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': '①課題の認識（何が問題で、最終的にどうしたいのかを正しく捉える） ②課題の推論（何をするのか、何から始めるのか、仮説を立てて整理する） ③施策の執行（決めたタスクを決めた手順で行う）', 'href': None}]}
}
"""
import os
from utils import get_pages, send_slack_message
from datetime import datetime

NOTION_TOKEN = os.environ["NOTION_API_TOKEN"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


pages = get_pages(DATABASE_ID = DATABASE_ID, headers = headers )

today = datetime.now()
weekly_count = 0
weekly_memos  = ""
weekly_titles, monthly_titles, yearly_titles = [],[],[]

for i,page in enumerate(pages):
    props = page['properties']

    title = props['📙  Book Title']['select']['name']
    memo = props['📝  Highlight']['title'][0]['text']['content']
    raw_created_time = props['Created At']['created_time']
    datetime_object = datetime.strptime(raw_created_time , "%Y-%m-%dT%H:%M:%S.%fZ")
    day_diff = (today - datetime_object).days

    if day_diff <= 7:
        weekly_count += 1
        weekly_memos += f"{weekly_count}: {memo}\n"
        weekly_titles.append(title)
    if day_diff <= 31:
        monthly_titles.append(title)
    if day_diff <= 365:
        yearly_titles.append(title)

weekly_memos = weekly_memos[:-1] #文末の\nを削除

message = f"""あなたの読書記録は以下です。

今週: {len(set(weekly_titles))}
今月: {len(set(monthly_titles))}
今年: {len(set(yearly_titles))}

あなたの今週の気づきは以下です。

{weekly_memos}
"""

print(message)
send_slack_message(text=message)
print("Success!!")


