import socket
from datetime import datetime


def start_listening(host, port):
    """Écoute et affiche les messages reçus"""
    try:
        # Créer un socket TCP/IP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Permettre la réutilisation de l'adresse
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Lier le socket à l'adresse et au port
        server_socket.bind((host, port))

        # Écouter les connexions entrantes (max 5 en attente)
        server_socket.listen(5)

        print(f"=== Serveur en écoute sur {host}:{port} ===")
        print("En attente de signaux...\n")

        while True:
            # Accepter une connexion
            client_socket, client_address = server_socket.accept()

            try:
                # Recevoir les données
                data = client_socket.recv(1024).decode('utf-8')

                if data:
                    # Afficher le message avec horodatage
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] Signal reçu de {client_address[0]}:")
                    print(f"  → {data}")
                    print()

            except Exception as e:
                print(f"Erreur lors de la réception: {e}")

            finally:
                # Fermer la connexion client
                client_socket.close()

    except KeyboardInterrupt:
        print("\nArrêt du serveur...")
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        server_socket.close()


def main():
    # Configuration
    HOST = '0.0.0.0'  # Écouter sur toutes les interfaces réseau
    PORT = 5000  # Port d'écoute (doit correspondre à l'émetteur)

    print("=== Script de réception de signaux ===")
    print("Appuyez sur Ctrl+C pour arrêter\n")

    # Afficher l'IP locale
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"Votre IP locale: {local_ip}")
    except:
        print("Impossible de déterminer l'IP locale")

    print(f"Port d'écoute: {PORT}\n")

    # Démarrer l'écoute
    start_listening(HOST, PORT)


if __name__ == "__main__":
    main()