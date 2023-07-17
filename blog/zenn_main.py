import time 
import requests
from bs4 import BeautifulSoup

# ZennのユーザーページのURL
url = "https://zenn.dev/sergicalsix"

# ページのHTMLを取得
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 各記事のタイトルと作成日時を取得
articles = soup.select('.ArticleCard')
for article in articles:
    title = article.select_one('.ArticleCard_title').text
    date = article.select_one('.ArticleCard_date').text
    print(f'Title: {title}\nDate: {date}\n')

# 各記事へのリンクを取得
article_links = [a['href'] for a in soup.select('.ArticleCard_link')]

print(article_links)

# 各記事のページを訪れて詳細情報を取得
for link in article_links:
    time.sleep(1)
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 記事のタイトル、作成日時、タグ、いいねの数を取得
    title = soup.select_one('.ArticlePage_headerTitle').text
    date = soup.select_one('.ArticlePage_headerDate').text
    tags = [tag.text for tag in soup.select('.ArticlePage_tags a')]
    likes = soup.select_one('.ArticlePage_likeCount').text
    
    print(f'Title: {title}\nDate: {date}\nTags: {tags}\nLikes: {likes}\n')
