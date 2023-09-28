from googleapiclient.discovery import build
import csv

# YouTube API 키 설정
API_KEY = input("Enter your YouTube API key: ")

# YouTube API 클라이언트 생성
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_videos():
    search_keyword = input("Enter Search Keyword: ")
    max_results = 30

    search_response = youtube.search().list(
        q=search_keyword,
        type='video',
        part='id,snippet',
        maxResults=max_results,
        order='viewCount'
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        video_id = search_result['id']['videoId']
        video_title = search_result['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        thumbnail_url = search_result['snippet']['thumbnails']['high']['url']
        
        videos.append([video_title, video_url, thumbnail_url])


    # CSV 파일로 저장
    with open('Resources/videos.csv', 'w',encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Title', 'URL', 'Thumbnail URL'])
        csv_writer.writerows(videos)

    return videos



if __name__ == '__main__':
    get_videos()