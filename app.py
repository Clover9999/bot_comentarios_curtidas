import os
import time
import random
import shutil
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Arquivos de autenticação OAuth para cada conta
CREDENTIALS_FILES = ["client_secrets.json", "client_secrets_2.json"]
TOKEN_FILE = "token.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# ID do vídeo
VIDEO_ID = "GQrnbLUXToY"

# Lista de comentários
COMMENTS = [
    "Ótimo vídeo! 🔥",
    "Conteúdo incrível! 😃",
    "Muito bom, continue assim! 🚀"
]

def create_client_secrets_2():
    """Verifica se o arquivo client_secrets_2.json existe e cria caso não exista."""
    if not os.path.exists(CREDENTIALS_FILES[1]):
        # Copia o arquivo client_secrets.json para client_secrets_2.json
        if os.path.exists(CREDENTIALS_FILES[0]):
            shutil.copy(CREDENTIALS_FILES[0], CREDENTIALS_FILES[1])
            print(f"✔ Arquivo {CREDENTIALS_FILES[1]} criado com sucesso a partir de {CREDENTIALS_FILES[0]}")
        else:
            print(f"❌ Erro: O arquivo {CREDENTIALS_FILES[0]} não foi encontrado!")
    else:
        print(f"✔ O arquivo {CREDENTIALS_FILES[1]} já existe.")

def get_authenticated_service(credentials_file):
    """Autentica no YouTube com um arquivo de credenciais específico."""
    creds = None

    # Deleta token para forçar novo login
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)

    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
    creds = flow.run_local_server(port=0)

    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)

def like_video(youtube):
    """Curte o vídeo."""
    try:
        youtube.videos().rate(id=VIDEO_ID, rating="like").execute()
        print("✔ Vídeo curtido com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao curtir o vídeo: {e}")
        print(f"Detalhes do erro: {e.args}")

def comment_video(youtube):
    """Comenta no vídeo."""
    try:
        comment = random.choice(COMMENTS)
        request = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": VIDEO_ID,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": comment
                        }
                    }
                }
            }
        )
        request.execute()
        print(f"✔ Comentário enviado: {comment}")
    except Exception as e:
        print(f"❌ Erro ao comentar no vídeo: {e}")
        print(f"Detalhes do erro: {e.args}")

# Verificar e criar client_secrets_2.json se necessário
create_client_secrets_2()

# Loop para trocar de conta automaticamente
for credentials_file in CREDENTIALS_FILES:
    print(f"🔄 Autenticando com {credentials_file}...")
    
    try:
        youtube = get_authenticated_service(credentials_file)
        
        like_video(youtube)
        comment_video(youtube)

        print("🔄 Trocando de conta...\n")
        time.sleep(5)  # Pequena pausa antes de trocar de conta
    
    except Exception as e:
        print(f"❌ Erro ao autenticar ou realizar ações com a conta {credentials_file}: {e}")
        print(f"Detalhes do erro: {e.args}")
