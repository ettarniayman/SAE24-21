#!/usr/bin/env python3
"""
fetch_destination_images.py
-----------------------------
Pour chaque destination de RTVoyage :
1. Recherche une photo pertinente via l'API Pexels (libre de droit)
2. Télécharge le fichier (image principale + une miniature)
3. Génère le SQL UPDATE pour remplir image_main / image_thumb
4. Génère aussi des INSERT INTO medias pour 2-3 photos de galerie par destination

Usage (depuis la racine du projet SAE24-21) :
    1. Crée un fichier .env avec : PEXELS_API_KEY=ta_cle_ici
    2. pip install requests python-dotenv --break-system-packages
    3. python3 scripts/fetch_destination_images.py

Sortie :
    - flask/app/static/images/destinations/<slug>-main.jpg
    - flask/app/static/images/destinations/<slug>-thumb.jpg
    - flask/app/static/images/destinations/<slug>-gallery-1.jpg / -2.jpg / -3.jpg
    - database/seed/seed_images.sql (à exécuter après seed.sql)
"""

import os
import re
import time
import sys
from pathlib import Path
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
try:
    import requests
except ImportError:
    print("Installe requests : pip install requests --break-system-packages")
    sys.exit(1)

# ────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ────────────────────────────────────────────────────────────────────

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")
PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"

# Chemins relatifs à la racine du projet (lance ce script depuis la racine SAE24-21)
IMAGES_DIR = Path("flask/app/static/images/destinations")
SQL_OUTPUT = Path("database/seed/seed_images.sql")

# Nombre de photos de galerie à récupérer en plus de l'image principale
GALLERY_COUNT = 3

# Délai entre requêtes pour respecter le rate limit Pexels (200 req/heure en free tier)
REQUEST_DELAY = 1.2

# ────────────────────────────────────────────────────────────────────
# Liste des destinations : (slug, requête de recherche optimisée)
# La requête inclut souvent le nom + un mot-clé géographique pour éviter
# les résultats génériques ou ambigus (ex: "Venice" pourrait remonter
# Venice Beach Californie sans précision).
# ────────────────────────────────────────────────────────────────────

DESTINATIONS = [
    ("marrakech", "Marrakech Morocco medina"),
    ("casablanca", "Casablanca Morocco city"),
    ("rabat", "Rabat Morocco"),
    ("fes", "Fes Morocco medina"),
    ("meknes", "Meknes Morocco"),
    ("tanger", "Tangier Morocco"),
    ("chefchaouen", "Chefchaouen blue city Morocco"),
    ("agadir", "Agadir Morocco beach"),
    ("essaouira", "Essaouira Morocco"),
    ("ouarzazate", "Ouarzazate Morocco desert"),
    ("merzouga", "Merzouga Sahara desert dunes"),
    ("dakhla", "Dakhla Morocco lagoon"),
    ("ifrane", "Ifrane Morocco mountains"),
    ("al-hoceima", "Al Hoceima Morocco coast"),
    ("sale", "Sale Morocco"),
    ("sahara-erg-chebbi", "Erg Chebbi Sahara dunes Morocco"),
    ("haut-atlas", "High Atlas mountains Morocco"),
    ("vallee-ziz", "Ziz Valley Morocco oasis"),
    ("gorges-todra", "Todra Gorges Morocco canyon"),
    ("gorges-dades", "Dades Gorges Morocco"),
    ("vallee-ourika", "Ourika Valley Morocco"),
    ("moyen-atlas", "Middle Atlas Morocco forest"),
    ("vallee-draa", "Draa Valley Morocco palm"),
    ("paris", "Paris France Eiffel Tower"),
    ("nice", "Nice France Cote Azur"),
    ("barcelone", "Barcelona Spain"),
    ("madrid", "Madrid Spain"),
    ("seville", "Seville Spain"),
    ("lisbonne", "Lisbon Portugal"),
    ("porto", "Porto Portugal"),
    ("rome", "Rome Italy Colosseum"),
    ("venise", "Venice Italy canal"),
    ("florence", "Florence Italy"),
    ("amsterdam", "Amsterdam Netherlands canal"),
    ("prague", "Prague Czech Republic"),
    ("santorini", "Santorini Greece"),
    ("athenes", "Athens Greece Acropolis"),
    ("istanbul", "Istanbul Turkey"),
    ("cappadoce", "Cappadocia Turkey balloons"),
    ("reykjavik", "Reykjavik Iceland"),
    ("dubai", "Dubai UAE skyline"),
    ("abu-dhabi", "Abu Dhabi UAE"),
    ("petra", "Petra Jordan"),
    ("bangkok", "Bangkok Thailand"),
    ("phuket", "Phuket Thailand beach"),
    ("chiang-mai", "Chiang Mai Thailand temple"),
    ("tokyo", "Tokyo Japan"),
    ("kyoto", "Kyoto Japan temple"),
    ("osaka", "Osaka Japan"),
    ("bali", "Bali Indonesia rice terrace"),
    ("ubud", "Ubud Bali Indonesia"),
    ("hanoi", "Hanoi Vietnam"),
    ("ho-chi-minh", "Ho Chi Minh City Vietnam"),
    ("halong-bay", "Ha Long Bay Vietnam"),
    ("maldives", "Maldives overwater villa"),
    ("new-york", "New York City skyline"),
    ("miami", "Miami Florida beach"),
    ("san-francisco", "San Francisco Golden Gate"),
    ("montreal", "Montreal Canada"),
    ("cancun", "Cancun Mexico beach"),
    ("rio", "Rio de Janeiro Brazil"),
    ("buenos-aires", "Buenos Aires Argentina"),
    ("cuzco", "Cusco Peru"),
    ("machu-picchu", "Machu Picchu Peru"),
    ("dakar", "Dakar Senegal"),
    ("serengeti", "Serengeti Tanzania safari"),
    ("zanzibar", "Zanzibar Tanzania beach"),
    ("sydney", "Sydney Australia opera house"),
]

# ────────────────────────────────────────────────────────────────────


def slugify_filename(slug: str, suffix: str) -> str:
    return f"{slug}-{suffix}.jpg"


def search_pexels(query: str, per_page: int = 5) -> list[dict]:
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page, "orientation": "landscape"}
    resp = requests.get(
    PEXELS_SEARCH_URL,
    headers=headers,
    params=params,
    timeout=15,
    verify=False)
    if resp.status_code != 200:
        print(f"  ⚠ Erreur Pexels ({resp.status_code}) pour '{query}': {resp.text[:200]}")
        return []
    data = resp.json()
    return data.get("photos", [])


def download_image(url: str, dest_path: Path) -> bool:
    try:
        resp = requests.get(url, timeout=20, verify=False)
        resp.raise_for_status()
        dest_path.write_bytes(resp.content)
        return True
    except Exception as e:
        print(f"  ⚠ Échec téléchargement {url}: {e}")
        return False


def escape_sql(text: str) -> str:
    return text.replace("'", "''")


def main():
    if not PEXELS_API_KEY:
        print("ERREUR: variable d'environnement PEXELS_API_KEY manquante.")
        print("Lance : export PEXELS_API_KEY=ta_cle   (Linux/Mac)")
        print("ou     : $env:PEXELS_API_KEY='ta_cle'   (PowerShell)")
        sys.exit(1)

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    sql_lines = [
        "-- Généré automatiquement par fetch_destination_images.py",
        "-- Photos libres de droit via l'API Pexels (https://www.pexels.com)",
        "-- Exécuter après seed.sql",
        "",
    ]

    for slug, query in DESTINATIONS:
        print(f"\n→ {slug} (recherche: '{query}')")
        photos = search_pexels(query, per_page=GALLERY_COUNT + 2)
        time.sleep(REQUEST_DELAY)

        if not photos:
            print(f"  ✗ Aucune photo trouvée pour {slug}, passage au suivant.")
            continue

        # Image principale = la première
        main_photo = photos[0]
        main_url = main_photo["src"]["large2x"]
        thumb_url = main_photo["src"]["medium"]
        photographer = main_photo.get("photographer", "Pexels")
        photographer_url = main_photo.get("photographer_url", "")

        main_filename = slugify_filename(slug, "main")
        thumb_filename = slugify_filename(slug, "thumb")

        ok_main = download_image(main_url, IMAGES_DIR / main_filename)
        time.sleep(REQUEST_DELAY)
        ok_thumb = download_image(thumb_url, IMAGES_DIR / thumb_filename)
        time.sleep(REQUEST_DELAY)

        if ok_main and ok_thumb:
            print(f"  ✓ Image principale + thumb téléchargées (photo: {photographer})")
            sql_lines.append(
                f"UPDATE destinations SET "
                f"image_main='/static/images/destinations/{main_filename}', "
                f"image_thumb='/static/images/destinations/{thumb_filename}' "
                f"WHERE slug='{slug}';"
            )

        # Galerie : les photos suivantes
        gallery_photos = photos[1:GALLERY_COUNT + 1]
        for i, photo in enumerate(gallery_photos, start=1):
            gallery_url = photo["src"]["large"]
            gallery_filename = slugify_filename(slug, f"gallery-{i}")
            ok = download_image(gallery_url, IMAGES_DIR / gallery_filename)
            time.sleep(REQUEST_DELAY)
            if ok:
                photographer_g = escape_sql(photo.get("photographer", "Pexels"))
                sql_lines.append(
                    f"INSERT INTO medias (filename, file_path, file_type, "
                    f"alt_text, media_category, destination_id, sort_order) "
                    f"SELECT '{gallery_filename}', "
                    f"'/static/images/destinations/{gallery_filename}', 'image', "
                    f"'Photo de {escape_sql(slug)} par {photographer_g} (Pexels)', "
                    f"'gallery', id, {i} FROM destinations WHERE slug='{slug}';"
                )
                print(f"  ✓ Galerie {i}/{len(gallery_photos)} téléchargée")

    SQL_OUTPUT.write_text("\n".join(sql_lines) + "\n", encoding="utf-8")
    print(f"\n\nTerminé. SQL généré dans : {SQL_OUTPUT}")
    print(f"Images téléchargées dans : {IMAGES_DIR}")
    print("\nPense à créditer Pexels et les photographes si exigé par leur licence "
          "(en général une mention discrète en footer suffit, vérifie pexels.com/license).")


if __name__ == "__main__":
    main()