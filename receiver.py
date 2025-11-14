import time
import os

# Même chemin que l'émetteur
SHARED_FILE = "C:\\Partage\\signaux.txt"  # Ou un chemin réseau comme "\\\\PC1\\Partage\\signaux.txt"


def watch_file():
    """Surveille le fichier et affiche les nouveaux messages"""

    # Position de lecture
    last_position = 0

    print("=== Récepteur de signaux (Fichier partagé) ===")
    print(f"Fichier surveillé: {SHARED_FILE}")
    print("En attente de nouveaux messages...\n")
    print("Appuyez sur Ctrl+C pour arrêter\n")

    # Attendre que le fichier existe
    while not os.path.exists(SHARED_FILE):
        print("⏳ En attente du fichier...")
        time.sleep(2)

    print("✓ Fichier détecté ! Surveillance active.\n")

    try:
        while True:
            try:
                # Lire le fichier
                with open(SHARED_FILE, "r", encoding="utf-8") as f:
                    # Aller à la dernière position lue
                    f.seek(last_position)

                    # Lire les nouvelles lignes
                    new_lines = f.readlines()

                    # Mettre à jour la position
                    last_position = f.tell()

                # Afficher les nouvelles lignes
                for line in new_lines:
                    line = line.strip()
                    if line and not line.startswith("==="):
                        print(f"📨 {line}")

            except Exception as e:
                print(f"⚠️  Erreur de lecture: {e}")

            time.sleep(1)  # Vérifie chaque seconde

    except KeyboardInterrupt:
        print("\n\nArrêt de la surveillance.")


if __name__ == "__main__":
    watch_file()