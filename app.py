import os
import time
import google.auth.exceptions
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from tkinter import messagebox

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN_FILE = "token.json"
CLIENT_SECRET_FILE = "client_secrets.json"
VIDEO_ID = "GQrnbLUXToY"  # Substitua pelo ID do vídeo que deseja interagir
COMENTARIO = "Ótimo vídeo! 😃🔥"

def get_authenticated_service():
    """Autentica e retorna o serviço do YouTube"""
    creds = None

    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            if not creds.valid:
                raise google.auth.exceptions.DefaultCredentialsError("Credenciais inválidas.")
        except (google.auth.exceptions.DefaultCredentialsError, ValueError):
            print("Token inválido! Excluindo e gerando um novo...")
            os.remove(TOKEN_FILE)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)

def like_video(youtube, video_id):
    """Curte o vídeo"""
    try:
        youtube.videos().rate(id=video_id, rating="like").execute()
        print(f"✔ Vídeo {video_id} curtido com sucesso!")
    except Exception as e:
        print(f"Erro ao curtir o vídeo: {e}")

def comment_video(youtube, video_id, comment):
    """Comenta no vídeo"""
    try:
        request = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {"textOriginal": comment}
                    }
                }
            },
        )
        request.execute()
        print(f"✔ Comentário enviado: {comment}")
    except Exception as e:
        print(f"Erro ao comentar no vídeo: {e}")

def logout():
    """Desloga do YouTube removendo o token e solicita nova autenticação"""
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        print("🔄 Deslogado com sucesso. Alternando para outra conta...")

def login_with_new_account():
    """Força logout e reautentica com outra conta"""
    logout()
    return get_authenticated_service()

# Loop principal para alternância de contas
if __name__ == "__main__":
    while True:
        youtube = get_authenticated_service()

        # Curtir e comentar o vídeo
        like_video(youtube, VIDEO_ID)
        comment_video(youtube, VIDEO_ID, COMENTARIO)

        # Esperar alguns segundos antes de alternar a conta
        time.sleep(3)

        # Perguntar se deseja trocar de conta
        escolha = input("Deseja trocar de conta e repetir? (s/n): ").strip().lower()
        if escolha == "s":
            youtube = login_with_new_account()
        else:
            print("✅ Finalizando o bot.")
            break
