import os
import requests
import json

API_TOKEN = os.environ['QIITA_API_TOKEN']


url = "https://qiita.com/api/v2/users/sergicalsix/items"
response = requests.get(url)


if response.status_code == 200:
    items_info = json.loads(response.text)

    # 各記事の情報を出力
    for item in items_info:
        print(item.keys())
        
else:
    print("エラーが発生しました。ステータスコード:", response.status_code)


"""
'created_at'
'tags'
'title'
'likes_count'
'url'

"""