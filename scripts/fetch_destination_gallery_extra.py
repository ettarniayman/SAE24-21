#!/usr/bin/env python3
"""
fetch_destination_gallery_extra.py
------------------------------------
Complement de fetch_destination_images.py : ajoute 4 photos de galerie
supplementaires par destination (sort_order 4 a 7), en plus des 3 deja
presentes, pour enrichir visuellement les pages detail destination.

Usage (depuis la racine du projet SAE24-21) :
    1. export PEXELS_API_KEY=ta_cle   (ou $env:PEXELS_API_KEY='ta_cle' en PowerShell)
    2. pip install requests --break-system-packages
    3. python3 scripts/fetch_destination_gallery_extra.py

Sortie :
    - flask/app/static/images/destinations/<slug>-gallery-4.jpg ... -7.jpg
    - database/seed/seed_gallery_extra.sql (a executer apres seed.sql)
"""

import os
import sys
import time
from pathlib import Path
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
try:
    import requests
except ImportError:
    print("Installe requests : pip install requests --break-system-packages")
    sys.exit(1)

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")
PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"

IMAGES_DIR = Path("flask/app/static/images/destinations")
SQL_OUTPUT = Path("database/seed/seed_gallery_extra.sql")

EXTRA_COUNT = 4
START_SORT_ORDER = 4
REQUEST_DELAY = 1.2

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


def search_pexels(query: str, per_page: int) -> list[dict]:
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page, "orientation": "landscape"}
    resp = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params, timeout=15, verify=False)
    if resp.status_code != 200:
        print(f"  ⚠ Erreur Pexels ({resp.status_code}) pour '{query}': {resp.text[:200]}")
        return []
    return resp.json().get("photos", [])


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
        sys.exit(1)

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    sql_lines = [
        "-- Généré automatiquement par fetch_destination_gallery_extra.py",
        "-- Photos libres de droit via l'API Pexels (https://www.pexels.com)",
        "-- Exécuter après seed.sql et seed_images.sql",
        "",
    ]

    for slug, query in DESTINATIONS:
        print(f"\n→ {slug}")
        # per_page un peu plus large pour eviter les doublons avec les 3 deja recuperees
        photos = search_pexels(query, per_page=EXTRA_COUNT + 3)
        time.sleep(REQUEST_DELAY)
        if not photos:
            print(f"  ✗ Aucune photo trouvée pour {slug}.")
            continue

        # On saute les 3 premieres (deja utilisees par fetch_destination_images.py: main + gallery-1/2/3)
        extra_photos = photos[3:3 + EXTRA_COUNT] or photos[:EXTRA_COUNT]
        for i, photo in enumerate(extra_photos, start=START_SORT_ORDER):
            filename = f"{slug}-gallery-{i}.jpg"
            ok = download_image(photo["src"]["large"], IMAGES_DIR / filename)
            time.sleep(REQUEST_DELAY)
            if not ok:
                continue
            photographer = escape_sql(photo.get("photographer", "Pexels"))
            sql_lines.append(
                f"INSERT INTO medias (filename, file_path, file_type, alt_text, media_category, destination_id, sort_order) "
                f"SELECT '{filename}', '/static/images/destinations/{filename}', 'image', "
                f"'Photo de {escape_sql(slug)} par {photographer} (Pexels)', "
                f"'gallery', id, {i} FROM destinations WHERE slug='{slug}';"
            )
            print(f"  ✓ gallery-{i} téléchargée (photo: {photographer})")

    SQL_OUTPUT.write_text("\n".join(sql_lines) + "\n", encoding="utf-8")
    print(f"\n\nTerminé. SQL généré dans : {SQL_OUTPUT}")
    print(f"Images téléchargées dans : {IMAGES_DIR}")


if __name__ == "__main__":
    main()
