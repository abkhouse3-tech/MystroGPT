from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

# Google Drive API scope
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def main():
    creds = None
    
    # पहले से credentials हैं तो load करो
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # अगर credentials नहीं हैं तो authorize करो
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:        
         flow = InstalledAppFlow.from_client_secrets_file(
        r"E:\MystroGPT\credentials\client_secret_691330242708-11inur50b643aqur0eo0jmjvltred1td.apps.googleusercontent.com.json",
    SCOPES

    )
    creds = flow.run_local_server(port=0)
    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)


    # Drive API service
    service = build("drive", "v3", credentials=creds)

    # कोई test file upload करो
    file_metadata = {"name": "test_upload.txt"}
    media = MediaFileUpload("script_hindi.json", mimetype="text/plain")
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    print("✅ File uploaded to Drive. File ID:", file.get("id"))

if __name__ == "__main__":
    main()
