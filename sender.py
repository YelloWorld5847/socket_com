import socket
import time


def send_signal(host, port, message):
    """Envoie un message texte à un destinataire"""
    try:
        # Créer un socket TCP/IP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Se connecter au serveur
        print(f"Connexion à {host}:{port}...")
        client_socket.connect((host, port))
        print("Connecté !")

        # Envoyer le message
        client_socket.send(message.encode('utf-8'))
        print(f"Message envoyé: {message}")

        # Fermer la connexion
        client_socket.close()

    except ConnectionRefusedError:
        print("Erreur: Connexion refusée. Vérifiez que le récepteur est en écoute.")
    except Exception as e:
        print(f"Erreur: {e}")


def main():
    # Configuration
    HOST = '192.168.1.167'  # Remplacer par l'IP du PC récepteur
    PORT = 5000  # Port d'écoute (doit correspondre au récepteur)

    print("=== Script d'envoi de signaux ===")
    print(f"Destination: {HOST}:{PORT}")
    print("Tapez 'quit' pour quitter\n")

    while True:
        # Demander le message à envoyer
        message = input("Message à envoyer: ")

        if message.lower() == 'quit':
            print("Fermeture...")
            break

        if message.strip():
            send_signal(HOST, PORT, message)
            time.sleep(0.5)  # Petite pause entre les envois
        else:
            print("Message vide, non envoyé.")


if __name__ == "__main__":
    main()