#!/usr/bin/env python3
"""
fetch_all_images.py
--------------------
Télécharge automatiquement les images Pexels pour TOUTES les sections
du site RTVoyage qui n'ont pas encore de photos :
  - Hôtels
  - Programmes
  - Articles de blog
  - Produits boutique

Met à jour la base de données PostgreSQL pour chaque section.

Usage :
    python3 fetch_all_images.py              → toutes les sections
    python3 fetch_all_images.py hotels       → hôtels uniquement
    python3 fetch_all_images.py programs     → programmes uniquement
    python3 fetch_all_images.py blog         → blog uniquement
    python3 fetch_all_images.py shop         → boutique uniquement

Prérequis :
    pip install requests psycopg2-binary

Configuration :
    Remplace PEXELS_API_KEY par ta vraie clé (gratuite sur pexels.com/api)
    Mets USE_PROXY = True si tu es sur le réseau IUT de Béthune
"""

import os
import sys
import time
import shutil
import requests
import psycopg2
import unicodedata
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# ──────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────
PEXELS_API_KEY = "gI8pYIAwo0fCZ284SLg7MsBsO2oFYCkE3X78Pncif3AaEWbtSPEsAD2c"

DB_CONFIG = {
    "host":     "127.0.0.1",
    "port":     "5432",
    "dbname":   "rtvoyage",
    "user":     "rtvoyage_user",
    "password": "rtvoyage_secret_2026",
}

STATIC_DIR = Path("flask/app/static/images")
USE_PROXY  = False
PROXY      = {
    "http":  "http://cache-etu.univ-artois.fr:3128",
    "https": "http://cache-etu.univ-artois.fr:3128",
}
SLEEP = 0.5   # secondes entre chaque requête Pexels


# ──────────────────────────────────────────────────────────────
# MOTS-CLÉS PERSONNALISÉS PAR ÉLÉMENT
# Pour les éléments non listés, le script génère une recherche automatique
# ──────────────────────────────────────────────────────────────

HOTEL_KEYWORDS = {
    "La Mamounia":                         "luxury palace hotel marrakech",
    "Royal Mansour":                       "luxury riad marrakech courtyard",
    "Sofitel Casablanca Tour Blanche":     "luxury hotel casablanca modern",
    "Palais Faraj Fès":                    "luxury riad fes medina",
    "Riad Assilah":                        "riad morocco blue white",
    "Kasbah Tamadot":                      "atlas mountains resort kasbah",
    "Le Méridien Dubaï":                   "luxury hotel dubai pool skyline",
    "Four Seasons Bali":                   "four seasons resort bali tropical pool",
    "Hôtel du Particulier":                "boutique hotel paris garden",
    "Grand Park Kodhipparu":               "overwater bungalow maldives luxury",
    "Sofitel Agadir Royal Bay Resort":     "beach resort agadir luxury pool",
    "Heure Bleue Palais":                  "riad essaouira blue boutique hotel",
    "Fairmont Tazi Palace Tangier":        "luxury palace hotel tangier",
    "Sofitel Rabat Jardin des Roses":      "luxury hotel rabat garden",
    "Dar Ahlam":                           "desert kasbah luxury lodge morocco",
    "Sahara Stars Camp":                   "desert luxury camp stars sahara",
    "Mandarin Oriental Bosphorus":         "luxury hotel istanbul bosphorus",
    "Katikies Santorini":                  "luxury hotel santorini caldera",
    "Tawaraya Ryokan":                     "japanese ryokan traditional kyoto",
    "Villa San Michele, A Belmond Hotel":  "tuscan villa florence luxury hotel",
    "Belmond Hotel Monasterio":            "colonial luxury hotel cusco peru",
}

PROGRAM_KEYWORDS = {
    # Programmes Maroc
    "Circuit des Villes Impériales":       "imperial cities morocco travel",
    "Sahara et Désert":                    "sahara desert dunes sunset camel",
    "Tour du Maroc":                       "morocco travel landscape mountains",
    # Programmes génériques
    "Safari":                              "african safari wildlife lions",
    "Croisière":                           "luxury cruise ship ocean",
    "City Break":                          "city travel urban weekend",
    "Trek":                                "mountain trekking hiking adventure",
    "Plage":                               "tropical beach luxury resort",
    "Culture":                             "cultural travel ancient ruins",
    "Aventure":                            "adventure travel outdoor nature",
    "Gastronomie":                         "gourmet food restaurant luxury",
}

BLOG_KEYWORDS = {
    "voyage":      "travel photography landscape adventure",
    "culture":     "cultural travel art museum",
    "gastronomie": "food gourmet restaurant local cuisine",
    "nature":      "nature landscape mountains forest",
    "plage":       "beach tropical ocean sunset",
    "aventure":    "adventure outdoor hiking exploration",
    "luxe":        "luxury travel hotel resort elegant",
    "desert":      "desert landscape dunes sunset",
    "montagne":    "mountains hiking alpine landscape",
    "ville":       "city skyline urban travel architecture",
}

SHOP_KEYWORDS = {
    "valise":      "luxury travel suitcase luggage",
    "sac":         "travel bag backpack quality",
    "accessoire":  "travel accessories elegant",
    "vêtement":    "travel clothing fashion",
    "bijou":       "jewelry accessories luxury",
    "parfum":      "perfume luxury bottle elegant",
    "livre":       "travel book photography",
    "tech":        "travel technology gadget",
    "default":     "luxury travel product elegant",
}


# ──────────────────────────────────────────────────────────────
# UTILITAIRES
# ──────────────────────────────────────────────────────────────

def make_slug(name: str) -> str:
    nfkd = unicodedata.normalize("NFKD", name.lower())
    ascii_str = nfkd.encode("ascii", "ignore").decode("ascii")
    slug = "".join(c if c.isalnum() else "-" for c in ascii_str)
    return "-".join(filter(None, slug.split("-")))


def get_pexels_image(query: str) -> str | None:
    """Cherche une image sur Pexels et retourne l'URL large."""
    headers = {"Authorization": PEXELS_API_KEY}
    params  = {"query": query, "per_page": 1, "orientation": "landscape"}
    proxies = PROXY if USE_PROXY else None
    try:
        resp = requests.get(
            "https://api.pexels.com/v1/search",
            headers=headers, params=params,
            proxies=proxies, timeout=15
        )
        resp.raise_for_status()
        photos = resp.json().get("photos", [])
        if not photos:
            return None
        return photos[0]["src"]["large"]
    except Exception as e:
        print(f"    ⚠️  Pexels '{query}' : {e}")
        return None


def download_image(url: str, dest: Path) -> bool:
    proxies = PROXY if USE_PROXY else None
    try:
        resp = requests.get(url, proxies=proxies, timeout=30, stream=True)
        resp.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"    ⚠️  Download : {e}")
        return False


def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Base de données connectée.")
        return conn
    except Exception as e:
        print(f"❌ Erreur BDD : {e}")
        print("   Si Docker tourne, remplace host par '127.0.0.1'")
        sys.exit(1)


def process_section(conn, section_name: str, rows: list, output_dir: Path,
                    keyword_fn, update_fn):
    """Traite une section générique : télécharge et met à jour."""
    print(f"\n{'='*60}")
    print(f"  📦 SECTION : {section_name.upper()} ({len(rows)} éléments)")
    print(f"{'='*60}")
    output_dir.mkdir(parents=True, exist_ok=True)

    ok = skip = err = 0
    for row in rows:
        item_id   = row[0]
        item_name = row[1]
        slug      = make_slug(item_name)
        main_path = output_dir / f"{slug}-main.jpg"
        db_path   = f"/static/images/{section_name}/{slug}-main.jpg"

        if main_path.exists():
            print(f"  ⏭️  [{item_id:02d}] {item_name} — déjà présente")
            update_fn(conn, item_id, db_path)
            skip += 1
            continue

        keyword = keyword_fn(item_name, row)
        print(f"  🔍 [{item_id:02d}] {item_name} → '{keyword}'")

        url = get_pexels_image(keyword)
        if not url:
            print(f"       ❌ Aucune image trouvée")
            err += 1
            continue

        if download_image(url, main_path):
            update_fn(conn, item_id, db_path)
            print(f"       ✅ {main_path.name}")
            ok += 1
        else:
            err += 1
        time.sleep(SLEEP)

    print(f"\n  Résultat {section_name} : ✅ {ok} téléchargés | ⏭️ {skip} existants | ❌ {err} erreurs")
    return ok, skip, err


# ──────────────────────────────────────────────────────────────
# SECTION HÔTELS
# ──────────────────────────────────────────────────────────────

def fetch_hotels(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM hotels ORDER BY id")
        rows = cur.fetchall()

    def keyword_fn(name, row):
        return HOTEL_KEYWORDS.get(name, f"luxury hotel {name}")

    def update_fn(conn, item_id, db_path):
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE hotels SET image_main=%s WHERE id=%s",
                (db_path, item_id)
            )
        conn.commit()

    return process_section(
        conn, "hotels", rows,
        STATIC_DIR / "hotels",
        keyword_fn, update_fn
    )


# ──────────────────────────────────────────────────────────────
# SECTION PROGRAMMES
# ──────────────────────────────────────────────────────────────

def fetch_programs(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name_fr FROM travel_programs ORDER BY id")
        rows = cur.fetchall()

    def keyword_fn(name, row):
        # Cherche d'abord un mot-clé exact, sinon par mots-clés du nom
        if name in PROGRAM_KEYWORDS:
            return PROGRAM_KEYWORDS[name]
        # Cherche une correspondance partielle
        name_lower = name.lower()
        for key, kw in PROGRAM_KEYWORDS.items():
            if key in name_lower:
                return kw
        return f"luxury travel tour {name}"

    def update_fn(conn, item_id, db_path):
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE travel_programs SET image_main=%s WHERE id=%s",
                (db_path, item_id)
            )
        conn.commit()

    return process_section(
        conn, "programs", rows,
        STATIC_DIR / "programs",
        keyword_fn, update_fn
    )


# ──────────────────────────────────────────────────────────────
# SECTION BLOG
# ──────────────────────────────────────────────────────────────

def fetch_blog(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, title_fr FROM blog_posts ORDER BY id")
        rows = cur.fetchall()

    def keyword_fn(name, row):
        name_lower = name.lower()
        for key, kw in BLOG_KEYWORDS.items():
            if key in name_lower:
                return kw
        return "travel photography landscape beautiful"

    def update_fn(conn, item_id, db_path):
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE blog_posts SET image_main=%s WHERE id=%s",
                (db_path, item_id)
            )
        conn.commit()

    return process_section(
        conn, "blog", rows,
        STATIC_DIR / "blog",
        keyword_fn, update_fn
    )


# ──────────────────────────────────────────────────────────────
# SECTION BOUTIQUE
# ──────────────────────────────────────────────────────────────

def fetch_shop(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name_fr FROM shop_products ORDER BY id")
        rows = cur.fetchall()

    def keyword_fn(name, row):
        name_lower = name.lower()
        for key, kw in SHOP_KEYWORDS.items():
            if key in name_lower:
                return kw
        return SHOP_KEYWORDS["default"]

    def update_fn(conn, item_id, db_path):
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE shop_products SET image_main=%s WHERE id=%s",
                (db_path, item_id)
            )
        conn.commit()

    return process_section(
        conn, "shop", rows,
        STATIC_DIR / "shop",
        keyword_fn, update_fn
    )


# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────

SECTIONS = {
    "hotels":   fetch_hotels,
    "programs": fetch_programs,
    "blog":     fetch_blog,
    "shop":     fetch_shop,
}

def main():
    print("=" * 60)
    print("  TÉLÉCHARGEMENT IMAGES — RTVoyage (toutes sections)")
    print("=" * 60)

    # Vérifier la clé Pexels
    if PEXELS_API_KEY == "VOTRE_CLE_API_PEXELS":
        print("\n❌ Tu dois renseigner ta clé Pexels dans PEXELS_API_KEY")
        print("   Crée un compte gratuit sur https://www.pexels.com/api/")
        sys.exit(1)

    # Sections à traiter
    args = sys.argv[1:]
    if args:
        sections_to_run = {k: v for k, v in SECTIONS.items() if k in args}
        if not sections_to_run:
            print(f"Sections disponibles : {', '.join(SECTIONS.keys())}")
            sys.exit(1)
    else:
        sections_to_run = SECTIONS

    conn = connect_db()

    total_ok = total_skip = total_err = 0
    for name, fn in sections_to_run.items():
        ok, skip, err = fn(conn)
        total_ok   += ok
        total_skip += skip
        total_err  += err

    conn.close()

    print(f"\n{'='*60}")
    print(f"  BILAN GLOBAL")
    print(f"  ✅ Téléchargés  : {total_ok}")
    print(f"  ⏭️  Déjà présents : {total_skip}")
    print(f"  ❌ Erreurs       : {total_err}")
    print(f"{'='*60}")
    print("\n✅ Redémarre Flask pour appliquer :")
    print("   docker-compose restart flask")


if __name__ == "__main__":
    main()