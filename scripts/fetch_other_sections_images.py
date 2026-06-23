#!/usr/bin/env python3
"""
fetch_other_sections_images.py
-------------------------------
Recupere une photo principale pour chaque hotel, programme, article de blog,
produit boutique et logo de compagnie aerienne, via l'API Pexels (libre de
droit), telecharge les fichiers et genere le SQL UPDATE correspondant.

Usage (depuis la racine du projet SAE24-21) :
    1. export PEXELS_API_KEY=ta_cle   (ou $env:PEXELS_API_KEY='ta_cle' en PowerShell)
    2. pip install requests --break-system-packages
    3. python3 scripts/fetch_other_sections_images.py

Sortie :
    - flask/app/static/images/uploads/<slug>.jpg (programs, blog, airlines)
    - flask/app/static/images/uploads/<slug>.jpg (hotels, shop products)
    - database/seed/seed_other_images.sql (a executer apres seed.sql)
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

UPLOADS_DIR = Path("flask/app/static/images/uploads")
SQL_OUTPUT = Path("database/seed/seed_other_images.sql")

REQUEST_DELAY = 1.2

# (table, slug_column, image_column, image_value_mode, items)
# image_value_mode: "absolute" -> /static/images/uploads/<file>  (hotels, shop_products)
#                    "filename" -> <file> only                   (travel_programs, blog_posts, airlines)
HOTELS = [
    ("la-mamounia-marrakech", "Mamounia palace hotel Marrakech luxury"),
    ("royal-mansour-marrakech", "Royal Mansour palace hotel Marrakech"),
    ("sofitel-casablanca", "Sofitel hotel tower Casablanca"),
    ("hotel-palais-fes", "luxury riad palace hotel Fes Morocco"),
    ("riad-chefchaouen", "riad hotel blue city Chefchaouen"),
    ("kasbah-tamadot-atlas", "kasbah luxury hotel Atlas mountains"),
    ("le-meridien-dubai", "luxury hotel Dubai skyline"),
    ("four-seasons-bali", "luxury resort hotel Bali"),
    ("hotel-particulier-paris", "boutique luxury hotel Paris"),
    ("grand-hotel-maldives", "overwater villa resort Maldives"),
    ("sofitel-agadir-royal-bay", "beach resort hotel Agadir"),
    ("heure-bleue-palais-essaouira", "riad palace hotel Essaouira"),
    ("fairmont-tazi-palace-tanger", "palace hotel Tangier"),
    ("sofitel-rabat-jardin-roses", "garden luxury hotel Rabat"),
    ("dar-ahlam-ouarzazate", "luxury kasbah hotel Ouarzazate desert"),
    ("sahara-stars-camp-merzouga", "luxury desert camp tent Sahara"),
    ("mandarin-oriental-bosphorus-istanbul", "luxury hotel Bosphorus Istanbul"),
    ("katikies-santorini", "white cliff hotel Santorini"),
    ("tawaraya-ryokan-kyoto", "traditional ryokan hotel Kyoto"),
    ("villa-san-michele-florence", "luxury villa hotel Florence Tuscany"),
    ("the-plaza-new-york", "luxury hotel facade New York"),
    ("park-hyatt-sydney", "luxury hotel harbour Sydney"),
    ("mandarin-oriental-prague", "luxury hotel Prague castle view"),
    ("belmond-hotel-monasterio-cuzco", "colonial luxury hotel Cusco"),
    ("tulia-zanzibar", "beach resort hotel Zanzibar"),
    ("singita-sasakwa-lodge-serengeti", "luxury safari lodge Serengeti"),
    ("copacabana-palace-rio", "luxury beach hotel Rio de Janeiro"),
    ("reykjavik-edition", "modern luxury hotel Reykjavik"),
]

PROGRAMS = [
    ("circuit-imperial-maroc", "Morocco imperial cities travel"),
    ("sahara-aventure", "Sahara desert adventure camel trek"),
    ("football-espagne", "football stadium Spain Bernabeu"),
    ("bali-spirituel", "Bali temple spiritual retreat"),
    ("tokyo-kyoto-culture", "Japan temple culture travel"),
    ("maldives-luxe", "Maldives honeymoon overwater bungalow"),
    ("cappadoce-istanbul", "Cappadocia hot air balloons Turkey"),
    ("aventure-atlas", "trekking Atlas mountains Morocco"),
    ("safari-tanzanie", "safari Tanzania wildlife"),
    ("gastronomie-italie", "Italy food gastronomy travel"),
]

BLOG_POSTS = [
    ("top-10-medinas-maroc", "Morocco medina street market"),
    ("guide-sahara-marocain", "Sahara desert dunes Morocco travel"),
    ("experience-football-espagne", "football stadium crowd Spain"),
    ("gastronomie-marocaine-secrets", "Moroccan cuisine tagine cooking"),
]

SHOP_PRODUCTS = [
    ("valise-cabine-premium", "premium cabin luggage suitcase"),
    ("sac-dos-trek-45l", "trekking backpack travel"),
    ("guide-maroc-lonely-planet", "travel guidebook Morocco"),
    ("tajine-decoratif", "decorative Moroccan tagine pottery"),
    ("adaptateur-universel", "universal travel power adapter"),
]

AIRLINES = [
    ("royal-air-maroc", "airplane sky aviation"),
    ("air-france", "airplane sky aviation"),
    ("emirates", "airplane sky aviation"),
    ("qatar-airways", "airplane sky aviation"),
    ("turkish-airlines", "airplane sky aviation"),
    ("ryanair", "airplane sky aviation"),
    ("easyjet", "airplane sky aviation"),
    ("transavia", "airplane sky aviation"),
]


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


def process_section(table: str, slug_col: str, image_col: str, mode: str, items: list[tuple], sql_lines: list[str]) -> None:
    print(f"\n=== {table} ===")
    for slug, query in items:
        print(f"→ {slug}")
        photos = search_pexels(query)
        time.sleep(REQUEST_DELAY)
        if not photos:
            print(f"  ✗ Aucune photo trouvée pour {slug}.")
            continue

        photo = photos[0]
        filename = f"{slug}.jpg"
        ok = download_image(photo["src"]["large"], UPLOADS_DIR / filename)
        time.sleep(REQUEST_DELAY)
        if not ok:
            continue

        value = f"/static/images/uploads/{filename}" if mode == "absolute" else filename
        sql_lines.append(
            f"UPDATE {table} SET {image_col}='{value}' WHERE {slug_col}='{slug}';"
        )
        photographer = photo.get("photographer", "Pexels")
        print(f"  ✓ téléchargée (photo: {photographer})")


def main():
    if not PEXELS_API_KEY:
        print("ERREUR: variable d'environnement PEXELS_API_KEY manquante.")
        sys.exit(1)

    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    sql_lines = [
        "-- Généré automatiquement par fetch_other_sections_images.py",
        "-- Photos libres de droit via l'API Pexels (https://www.pexels.com)",
        "-- Exécuter après seed.sql",
        "",
    ]

    process_section("hotels", "slug", "image_main", "absolute", HOTELS, sql_lines)
    process_section("travel_programs", "slug", "image_main", "filename", PROGRAMS, sql_lines)
    process_section("blog_posts", "slug", "image_main", "filename", BLOG_POSTS, sql_lines)
    process_section("shop_products", "slug", "image_main", "absolute", SHOP_PRODUCTS, sql_lines)
    process_section("airlines", "slug", "logo", "filename", AIRLINES, sql_lines)

    SQL_OUTPUT.write_text("\n".join(sql_lines) + "\n", encoding="utf-8")
    print(f"\n\nTerminé. SQL généré dans : {SQL_OUTPUT}")
    print(f"Images téléchargées dans : {UPLOADS_DIR}")


if __name__ == "__main__":
    main()
