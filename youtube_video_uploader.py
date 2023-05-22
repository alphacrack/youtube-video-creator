from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
#create logger
import logging
logger = logging.getLogger('youtube_video_creator')
logger.setLevel(logging.DEBUG)
logging_handler = logging.StreamHandler()
logging_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging_handler.setFormatter(formatter)
logger.addHandler(logging_handler)

scopes = ['https://www.googleapis.com/auth/youtube.upload']

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
credentials = flow.run_local_server(port=0)

youtube = build('youtube', 'v3', credentials=credentials)

def upload_video(video_path, title, description, tags):
    try:
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '22'
            },
            'status' : {
                'privacyStatus': 'public'
            }
        }
        media = MediaFileUpload(video_path)

        response = youtube.videos().insert(
            part = 'snippet,status',
            body = request_body,
            media_body = media
        ).execute()
        logger.info('Video uploaded succesfully')
        return response['id']
    except Exception as exc:
        logger.error(exc)
        return False
    return True

if __name__ == '__main__':
    video_path = 'output.mp4'
    title = 'Hello from TLA'
    description = 'This video is output of automation'
    tags = ['python', 'youtube', 'automation']
    if upload_video(video_path, title, description, tags):
        logger.info("Video Uploaded")
    else:
        "Issue with Upload"


