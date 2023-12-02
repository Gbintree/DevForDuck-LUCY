import csv
import requests

from datetime import datetime

from googleapiclient.discovery import build

# YouTube API 키 설정
API_KEY = input("Enter your YouTube API key: ")

# YouTube API 클라이언트 생성
youtube = build('youtube', 'v3', developerKey=API_KEY)


def save_search_result_csv(result_list):
    
    folder_name = input("Enter Folder Name: ")

    videos = [] 

    for search_result in result_list.get('items', []):
        video_id = search_result['id']['videoId']
        video_title = search_result['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        thumbnail_url = search_result['snippet']['thumbnails']['high']['url']

        videos.append([video_id,video_title, video_url, thumbnail_url])

    # CSV 파일로 저장
    with open(f'Resources/{folder_name}/videos.csv', 'w',encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile) # (csvfile,quoting=csv.QUOTE_NONE, escapechar='\\')
        csv_writer.writerow(['Video ID','Title', 'URL', 'Thumbnail URL'])
        csv_writer.writerows(videos)



def save_img_from_url(local_filename,url):
    image_save_directory = f'Resources/Images/{local_filename}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # 요청이 성공하면 계속 진행

        with open(image_save_directory, 'wb') as file:
            file.write(response.content)

        print(f'Image saved at directory: {image_save_directory}')

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP Error: {http_err}')

    except Exception as err:
        print(f'Error: {err}')

def get_videos_from_designated_channel():
    channel_id = input("Enter Channel ID: ")
    folder_name = input("Enter Folder Name: ")
    max_results = 20
    videos_response = youtube.search().list(
        channelId=channel_id,
        type='video',
        part='id,snippet',
        maxResults=max_results,
        order='viewCount'
    ).execute()

    save_search_result_csv(videos_response)

def get_videos_with_date_filter():
    # 원하는 날짜 및 시간을 ISO 8601 형식으로 변환합니다. (예: 2023-01-01T00:00:00Z)
    published_after_date = datetime(2023, 1, 1).isoformat() + 'Z'
    published_before_date = datetime(2023, 11, 5).isoformat() + 'Z'

    search_keyword = input("Enter Search Keyword: ")
    folder_name = input("Enter Folder Name: ")
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
        
        videos.append([video_id,video_title, video_url, thumbnail_url])

    # CSV 파일로 저장
    with open(f'Resources/{folder_name}/videos.csv', 'w',encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile) # (csvfile,quoting=csv.QUOTE_NONE, escapechar='\\')
        csv_writer.writerow(['Video ID','Title', 'URL', 'Thumbnail URL'])
        csv_writer.writerows(videos)

    return videos   

def get_videos():
    search_keyword = input("Enter Search Keyword: ")
    folder_name = input("Enter Folder Name: ")
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
        
        videos.append([video_id,video_title, video_url, thumbnail_url])

        thumbnail_filename = f'{video_id}.png' # f'Resources/Images/{video_id}.png'

        # save_img_from_url(thumbnail_filename,thumbnail_url)

    

    # CSV 파일로 저장
    with open(f'Resources/{folder_name}/videos.csv', 'w',encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile) # (csvfile,quoting=csv.QUOTE_NONE, escapechar='\\')
        csv_writer.writerow(['Video ID','Title', 'URL', 'Thumbnail URL'])
        csv_writer.writerows(videos)

    return videos



if __name__ == '__main__':
    get_videos()
    # get_videos_with_date_filter()
    # get_videos_from_designated_channel()