import os
import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError

# Configurações de autenticação
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
CLIENT_SECRET_FILE = "client_secrets.json"
TOKEN_FILE = "token.json"

def get_authenticated_service():
    """Autentica e retorna o serviço da API do YouTube."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds, _ = google.auth.load_credentials_from_file(TOKEN_FILE, scopes=SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    
    return build("youtube", "v3", credentials=creds)

def like_video(youtube, video_id):
    """Curte um vídeo do YouTube."""
    try:
        youtube.videos().rate(id=video_id, rating="like").execute()
        print(f"✔ Vídeo {video_id} curtido com sucesso!")
    except HttpError as e:
        print(f"❌ Erro ao curtir vídeo: {e}")

def comment_video(youtube, video_id, comment_text):
    """Comenta em um vídeo do YouTube."""
    try:
        request = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": comment_text
                        }
                    }
                }
            }
        )
        response = request.execute()
        print(f"✔ Comentário enviado: {comment_text}")
    except HttpError as e:
        print(f"❌ Erro ao comentar no vídeo: {e}")

def subscribe_channel(youtube, channel_id):
    """Inscreve-se em um canal do YouTube, evitando autoinscrição."""
    try:
        # Obtém o ID do usuário autenticado
        user_response = youtube.channels().list(part="id", mine=True).execute()
        my_channel_id = user_response["items"][0]["id"]
        
        if my_channel_id == channel_id:
            print("❌ Erro: Você não pode se inscrever no seu próprio canal.")
            return

        request = youtube.subscriptions().insert(
            part="snippet",
            body={
                "snippet": {
                    "resourceId": {
                        "kind": "youtube#channel",
                        "channelId": channel_id
                    }
                }
            }
        )
        response = request.execute()
        print(f"✔ Inscrito com sucesso no canal {channel_id}!")
    except HttpError as e:
        print(f"❌ Erro ao se inscrever no canal: {e}")

if __name__ == "__main__":
    youtube = get_authenticated_service()
    
    VIDEO_ID = "Eyau-w3Xqkw"  # Substitua pelo ID do vídeo desejado
    CHANNEL_ID = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Substitua pelo ID do canal desejado
    COMMENT_TEXT = "Ótimo vídeo! 😃🔥"
    
    like_video(youtube, VIDEO_ID)
    comment_video(youtube, VIDEO_ID, COMMENT_TEXT)
    subscribe_channel(youtube, CHANNEL_ID)
