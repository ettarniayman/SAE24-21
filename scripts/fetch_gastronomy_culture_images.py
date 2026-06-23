#!/usr/bin/env python3
"""
fetch_gastronomy_culture_images.py
-----------------------------------
Complement de fetch_destination_images.py : recupere 1 photo par destination
illustrant la gastronomie locale et 1 photo illustrant la culture/architecture,
via l'API Pexels (libre de droit), pour illustrer les onglets Gastronomie et
Culture de la page detail destination.

Usage (depuis la racine du projet SAE24-21) :
    1. Variable d'environnement PEXELS_API_KEY deja utilisee par
       fetch_destination_images.py (meme cle)
    2. pip install requests --break-system-packages
    3. python3 scripts/fetch_gastronomy_culture_images.py

Sortie :
    - flask/app/static/images/destinations/<slug>-gastronomy.jpg
    - flask/app/static/images/destinations/<slug>-culture.jpg
    - database/seed/seed_gastronomy_culture.sql (a executer apres seed.sql)
"""

import os
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

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")
PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"

IMAGES_DIR = Path("flask/app/static/images/destinations")
SQL_OUTPUT = Path("database/seed/seed_gastronomy_culture.sql")

REQUEST_DELAY = 1.2

# Memes destinations que fetch_destination_images.py, avec requetes ciblees
# gastronomy / culture distinctes du nom de la destination seul.
DESTINATIONS = [
    ("marrakech", "Moroccan tagine food", "Marrakech medina architecture"),
    ("casablanca", "Moroccan cuisine couscous", "Casablanca Hassan II mosque architecture"),
    ("rabat", "Moroccan mint tea pastry", "Rabat kasbah architecture"),
    ("fes", "Moroccan pastilla food", "Fes medina pottery craft"),
    ("meknes", "Moroccan tagine olives", "Meknes Bab Mansour gate architecture"),
    ("tanger", "Moroccan seafood pastilla", "Tangier medina architecture"),
    ("chefchaouen", "Moroccan tagine food", "Chefchaouen blue city architecture"),
    ("agadir", "Moroccan grilled fish food", "Agadir kasbah architecture"),
    ("essaouira", "Moroccan seafood grill", "Essaouira ramparts architecture"),
    ("ouarzazate", "Moroccan tagine dates", "Ouarzazate kasbah architecture"),
    ("merzouga", "Moroccan desert bread food", "Merzouga berber tent culture"),
    ("dakhla", "Moroccan oysters seafood", "Dakhla lagoon culture"),
    ("ifrane", "Moroccan mountain food", "Ifrane alpine architecture"),
    ("al-hoceima", "Moroccan Mediterranean food", "Al Hoceima coast architecture"),
    ("sale", "Moroccan traditional food", "Sale medina architecture"),
    ("sahara-erg-chebbi", "Moroccan desert tagine", "Sahara berber culture tent"),
    ("haut-atlas", "Moroccan berber food", "High Atlas berber village culture"),
    ("vallee-ziz", "Moroccan date palm food", "Ziz valley oasis culture"),
    ("gorges-todra", "Moroccan tagine food", "Todra gorges berber culture"),
    ("gorges-dades", "Moroccan tagine food", "Dades valley kasbah architecture"),
    ("vallee-ourika", "Moroccan berber tea", "Ourika valley berber culture"),
    ("moyen-atlas", "Moroccan mountain cuisine", "Middle Atlas berber culture"),
    ("vallee-draa", "Moroccan dates food", "Draa valley palm grove culture"),
    ("paris", "French pastry croissant", "Paris architecture monument"),
    ("nice", "French Riviera food", "Nice old town architecture"),
    ("barcelone", "Spanish tapas food", "Barcelona Gaudi architecture"),
    ("madrid", "Spanish tapas food", "Madrid architecture monument"),
    ("seville", "Spanish tapas food", "Seville flamenco culture"),
    ("lisbonne", "Portuguese pastry food", "Lisbon tram architecture"),
    ("porto", "Portuguese seafood food", "Porto riverside architecture"),
    ("rome", "Italian pasta food", "Rome colosseum architecture"),
    ("venise", "Italian seafood food", "Venice canal architecture"),
    ("florence", "Italian food Tuscany", "Florence renaissance architecture"),
    ("amsterdam", "Dutch food cheese", "Amsterdam canal houses architecture"),
    ("prague", "Czech food goulash", "Prague castle architecture"),
    ("santorini", "Greek food Santorini", "Santorini white architecture"),
    ("athenes", "Greek food souvlaki", "Athens acropolis architecture"),
    ("istanbul", "Turkish food kebab", "Istanbul mosque architecture"),
    ("cappadoce", "Turkish food cuisine", "Cappadocia cave architecture"),
    ("reykjavik", "Icelandic food cuisine", "Reykjavik architecture culture"),
    ("dubai", "Arabic food cuisine", "Dubai skyline architecture"),
    ("abu-dhabi", "Arabic food cuisine", "Abu Dhabi mosque architecture"),
    ("petra", "Jordanian food cuisine", "Petra ancient architecture"),
    ("bangkok", "Thai street food", "Bangkok temple architecture"),
    ("phuket", "Thai seafood food", "Phuket temple culture"),
    ("chiang-mai", "Thai food cuisine", "Chiang Mai temple architecture"),
    ("tokyo", "Japanese sushi food", "Tokyo temple architecture"),
    ("kyoto", "Japanese food cuisine", "Kyoto temple architecture"),
    ("osaka", "Japanese street food", "Osaka castle architecture"),
    ("bali", "Indonesian food cuisine", "Bali temple culture"),
    ("ubud", "Indonesian food rice", "Ubud temple architecture"),
    ("hanoi", "Vietnamese food pho", "Hanoi temple architecture"),
    ("ho-chi-minh", "Vietnamese food cuisine", "Ho Chi Minh architecture"),
    ("halong-bay", "Vietnamese seafood food", "Ha Long Bay culture boat"),
    ("maldives", "Maldivian seafood food", "Maldives culture architecture"),
    ("new-york", "New York food cuisine", "New York architecture skyline"),
    ("miami", "Miami food cuisine", "Miami art deco architecture"),
    ("san-francisco", "San Francisco food", "San Francisco architecture culture"),
    ("montreal", "Montreal food poutine", "Montreal architecture culture"),
    ("cancun", "Mexican food cuisine", "Cancun Mayan architecture"),
    ("rio", "Brazilian food cuisine", "Rio de Janeiro architecture culture"),
    ("buenos-aires", "Argentinian food steak", "Buenos Aires architecture culture"),
    ("cuzco", "Peruvian food cuisine", "Cusco inca architecture"),
    ("machu-picchu", "Peruvian food cuisine", "Machu Picchu inca architecture"),
    ("dakar", "Senegalese food cuisine", "Dakar culture architecture"),
    ("serengeti", "Tanzanian food cuisine", "Serengeti maasai culture"),
    ("zanzibar", "Zanzibar spice food", "Zanzibar stone town architecture"),
    ("sydney", "Australian food cuisine", "Sydney opera house architecture"),
]


def slugify_filename(slug: str, suffix: str) -> str:
    return f"{slug}-{suffix}.jpg"


def search_pexels(query: str, per_page: int = 3) -> list[dict]:
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


def fetch_category(slug: str, query: str, category: str, sql_lines: list[str]) -> None:
    photos = search_pexels(query)
    time.sleep(REQUEST_DELAY)
    if not photos:
        print(f"  ✗ Aucune photo {category} trouvée pour {slug}.")
        return

    photo = photos[0]
    filename = slugify_filename(slug, category)
    ok = download_image(photo["src"]["large"], IMAGES_DIR / filename)
    time.sleep(REQUEST_DELAY)
    if not ok:
        return

    photographer = escape_sql(photo.get("photographer", "Pexels"))
    sql_lines.append(
        f"INSERT INTO medias (filename, file_path, file_type, alt_text, media_category, destination_id, sort_order) "
        f"SELECT '{filename}', '/static/images/destinations/{filename}', 'image', "
        f"'Photo {category} de {escape_sql(slug)} par {photographer} (Pexels)', "
        f"'{category}', id, 1 FROM destinations WHERE slug='{slug}';"
    )
    print(f"  ✓ {category} téléchargée (photo: {photographer})")


def main():
    if not PEXELS_API_KEY:
        print("ERREUR: variable d'environnement PEXELS_API_KEY manquante.")
        sys.exit(1)

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    sql_lines = [
        "-- Généré automatiquement par fetch_gastronomy_culture_images.py",
        "-- Photos libres de droit via l'API Pexels (https://www.pexels.com)",
        "-- Exécuter après seed.sql",
        "",
    ]

    for slug, gastronomy_query, culture_query in DESTINATIONS:
        print(f"\n→ {slug}")
        fetch_category(slug, gastronomy_query, "gastronomy", sql_lines)
        fetch_category(slug, culture_query, "culture", sql_lines)

    SQL_OUTPUT.write_text("\n".join(sql_lines) + "\n", encoding="utf-8")
    print(f"\n\nTerminé. SQL généré dans : {SQL_OUTPUT}")
    print(f"Images téléchargées dans : {IMAGES_DIR}")


if __name__ == "__main__":
    main()
