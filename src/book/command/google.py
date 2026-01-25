from googleapiclient.discovery import build
from book.args import BookArgs


def fetch(args: BookArgs):
    API_KEY = "AIzaSyCHaPTDzaOpGVWG06r56LAJagDGEjCZ42Y"

    # Initialisation du service
    service = build("books", "v1", developerKey=API_KEY, cache_discovery=False)

    # Exécution de la requête
    query = "intitle:Dune+inauthor:Herbert"
    request = service.volumes().list(q=query, maxResults=5)  # CORRECT
    response = request.execute()
    response = request.execute()

    # Parcours des résultats
    for item in response.get("items", []):
        volume_info = item.get("volumeInfo", {})
        print(f"Titre: {volume_info.get('title')}")
        print(f"Auteurs: {', '.join(volume_info.get('authors', []))}")
        print("-" * 20)
