import requests
import time
import json
import os
import platform


GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GIST_ID = "6ad1f414e4e4b4af15301e0a96c454ee"
SENDER_ID = "PC2"  # Changez en "PC1" sur l'autre PC
CHECK_INTERVAL = 3  # Secondes entre chaque vérification

class GistComm:
    def __init__(self, token, gist_id, sender_id):
        self.token = token
        self.gist_id = gist_id
        self.sender_id = sender_id
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.api_url = "https://api.github.com/gists"
        
        print(f"✓ ID : {self.sender_id}")
        if gist_id:
            print(f"✓ Gist ID : {gist_id}")
    
    def create_gist(self):
        """Crée un nouveau Gist (à faire une seule fois)"""
        data = {
            "description": "Communication inter-PC - Shutdown Remote",
            "public": False,
            "files": {
                "messages.json": {
                    "content": json.dumps({"messages": []})
                }
            }
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 201:
                result = response.json()
                self.gist_id = result['id']
                print(f"\n✓ Gist créé avec succès !")
                print(f"\n📋 COPIEZ CET ID dans le code :")
                print(f"   GIST_ID = \"{self.gist_id}\"")
                print(f"\n⚠️  Mettez le même ID sur les 2 PC !\n")
                return True
            else:
                print(f"✗ Erreur : {response.status_code}")
                print(response.text)
                return False
        except Exception as e:
            print(f"✗ Erreur : {e}")
            return False
    
    def send_message(self, content):
        if not self.gist_id:
            print("✗ Pas de Gist ID configuré")
            return False
        
        try:
            messages = self.get_messages()
            
            new_message = {
                'content': content,
                'sender': self.sender_id,
                'timestamp': time.time()
            }
            
            messages.append(new_message)
            
            if len(messages) > 100:
                messages = messages[-100:]
            
            data = {
                "files": {
                    "messages.json": {
                        "content": json.dumps({"messages": messages}, indent=2)
                    }
                }
            }
            
            response = requests.patch(
                f"{self.api_url}/{self.gist_id}",
                headers=self.headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✓ Envoyé")
                return True
            else:
                print(f"✗ Erreur : {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Erreur : {e}")
            return False
    
    def get_messages(self):
        """Récupère tous les messages"""
        if not self.gist_id:
            return []
        
        try:
            response = requests.get(
                f"{self.api_url}/{self.gist_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data['files']['messages.json']['content']
                return json.loads(content).get('messages', [])
            
            return []
            
        except Exception as e:
            print(f"Erreur lecture : {e}")
            return []
    
    def send_shutdown_command(self):
        """Envoie la commande SHUTDOWN"""
        print("\n📤 Envoi de la commande SHUTDOWN...")
        if self.send_message("SHUTDOWN"):
            print("✓ Commande envoyée ! L'autre PC va s'éteindre.")
        else:
            print("✗ Échec de l'envoi")

def main():
    if not GITHUB_TOKEN:
        print("\n⚠️  CONFIGURATION REQUISE :")
        print("1. Allez sur : https://github.com/settings/tokens")
        print("2. 'Generate new token (classic)'")
        print("3. Cochez uniquement 'gist'")
        print("4. Copiez le token dans le code")
        exit()
    
    comm = GistComm(GITHUB_TOKEN, GIST_ID, SENDER_ID)
    
    print("\n" + "=" * 60)
    print("MODES DISPONIBLES :")
    print("=" * 60)
    print("1. 📤 Envoyer commande SHUTDOWN (PC de contrôle)")
    print("2. 📨 Envoyer un message unique")
    
    if not GIST_ID:
        print("5. ⚙️  Créer un nouveau Gist (FAITES CECI EN PREMIER)")
    
    choice = input("\nChoix : ").strip()
    
    if choice == '1':
        # Envoyer la commande d'extinction
        comm.send_shutdown_command()

    elif choice == '2':
        msg = input("Message : ")
        comm.send_message("MSG " + msg)
        
    elif choice == '3':
        comm.create_gist()
    
    else:
        print("✗ Choix invalide")

if __name__ == '__main__':
    main()
