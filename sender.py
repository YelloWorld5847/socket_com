import time
from datetime import datetime
import os

# Chemin du fichier partagé (à adapter)
SHARED_FILE = "C:\\Partage\\signaux.txt"  # Ou un chemin réseau comme "\\\\PC2\\Partage\\signaux.txt"


def send_message(message):
    """Écrit le message dans le fichier partagé"""
    try:
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"

        # Écrire dans le fichier (ajout)
        with open(SHARED_FILE, "a", encoding="utf-8") as f:
            f.write(full_message)

        print(f"✓ Message envoyé: {message}")
        return True

    except Exception as e:
        print(f"✗ Erreur: {e}")
        print(f"   Vérifiez que le dossier existe et est accessible")
        return False


def main():
    print("=== Émetteur de signaux (Fichier partagé) ===")
    print(f"Fichier: {SHARED_FILE}")
    print("Tapez 'quit' pour quitter\n")

    # Créer le fichier s'il n'existe pas
    try:
        if not os.path.exists(SHARED_FILE):
            os.makedirs(os.path.dirname(SHARED_FILE), exist_ok=True)
            with open(SHARED_FILE, "w", encoding="utf-8") as f:
                f.write("=== Début des signaux ===\n\n")
    except Exception as e:
        print(f"⚠️  Erreur lors de la création du fichier: {e}\n")

    while True:
        message = input("Message: ")

        if message.lower() == 'quit':
            break

        if message.strip():
            send_message(message)

        time.sleep(0.2)


if __name__ == "__main__":
    main()