import os
import pickle
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_service():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle","rb") as f:
            creds = pickle.load(f)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)

        with open("token.pickle","wb") as f:
            pickle.dump(creds,f)

    return build("youtube","v3",credentials=creds)

def resumable_upload(request):
    response = None
    error = None
    retry = 0

    while response is None:
        try:
            status, response = request.next_chunk()

            if status:
                print(f"[DEBUG] Upload progress: {int(status.progress()*100)}%")

        except Exception as e:
            print("[ERROR]", str(e))
            retry += 1

            if retry > 5:
                raise Exception("Upload failed after retries")

            sleep_time = 2 ** retry
            print(f"[DEBUG] Retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)

    return response

def upload_video(file_path):
    print("[DEBUG] Uploading to YouTube (resumable)...")

    youtube = get_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet":{
                "title":"Only 1% Can Solve This 🤯",
                "description":"Try this brain puzzle!",
                "tags":["puzzle","brain","quiz","shorts"],
                "categoryId":"22"
            },
            "status":{"privacyStatus":"public"}
        },
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )

    response = resumable_upload(request)

    print("[DEBUG] Upload complete:", response.get("id"))
