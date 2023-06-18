import requests
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError



def send_slack_message(text = "Hello from your app! :tada:", channel = "random"):

    slack_token = os.environ["SLACK_API_TOKEN"]
    client = WebClient(token=slack_token)

    try:
        response = client.chat_postMessage(
            channel=channel,
            text=text
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"] 
	

def get_pages(DATABASE_ID, headers, num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 10_000 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results


#url = props["URL"]["title"][0]["text"]["content"]
#title = props["Title"]["rich_text"][0]["text"]["content"]
#published = props["Published"]["date"]["start"]
#published = datetime.fromisoformat(published)