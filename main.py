import os
from googleapiclient.discovery import build
from notion_client import Client
from datetime import datetime

def get_stats_and_save_notion():
    # 1. 열쇠들 꺼내기
    youtube_key = os.environ['YOUTUBE_API_KEY']
    channel_id = os.environ['CHANNEL_ID']
    notion_token = os.environ['NOTION_TOKEN']
    database_id = os.environ['NOTION_DATABASE_ID']

    # 2. 유튜브 데이터 가져오기
    youtube = build('youtube', 'v3', developerKey=youtube_key)
    request = youtube.channels().list(part='snippet,statistics', id=channel_id)
    response = request.execute()
    
    if not response['items']:
        print("채널을 찾을 수 없습니다.")
        return

    item = response['items'][0]
    title = item['snippet']['title']
    stats = item['statistics']
    today = datetime.now().strftime('%Y-%m-%d')

    # 3. 노션에 저장하기
    notion = Client(auth=notion_token)
    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "채널명": {"title": [{"text": {"content": title}}]},
            "날짜": {"date": {"start": today}},
            "구독자": {"number": int(stats['subscriberCount'])},
            "조회수": {"number": int(stats['viewCount'])},
            "영상수": {"number": int(stats['videoCount'])}
        }
    )
    print(f"{today} 데이터가 노션에 저장되었습니다!")

if __name__ == "__main__":
    get_stats_and_save_notion()
