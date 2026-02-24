import os
from googleapiclient.discovery import build

def get_stats():
    # 금고에서 열쇠 꺼내기
    api_key = os.environ['YOUTUBE_API_KEY']
    channel_id = os.environ['CHANNEL_ID']
    
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.channels().list(part='snippet,statistics', id=channel_id)
    response = request.execute()
    
    if response['items']:
        item = response['items'][0]
        title = item['snippet']['title']
        stats = item['statistics']
        
        # 화면에 출력 (나중에 노션으로 보낼 데이터입니다)
        print(f"--- {title} 채널 통계 ---")
        print(f"구독자 수: {stats['subscriberCount']}")
        print(f"전체 조회수: {stats['viewCount']}")
        print(f"업로드 영상: {stats['videoCount']}")
    else:
        print("채널을 찾을 수 없습니다.")

if __name__ == "__main__":
    get_stats()
