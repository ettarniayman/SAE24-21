# scripts/

Scripts utilitaires ponctuels pour RTVoyage (seed de données, migrations de données, nettoyage). Ils ne font pas partie de l'application Flask ni de la stack Docker — ils se lancent manuellement, en local, depuis la racine du projet.

## fetch_destination_images.py

Récupère une photo principale + miniature + galerie pour chaque destination via l'API Pexels, télécharge les fichiers et génère le SQL correspondant.

**Variable d'environnement requise :** `PEXELS_API_KEY` (clé API Pexels, gratuite sur pexels.com/api).

**Installation :**
```bash
pip install requests python-dotenv --break-system-packages
```

**Commande (depuis la racine du projet) :**
```bash
export PEXELS_API_KEY=ta_cle        # ou $env:PEXELS_API_KEY='ta_cle' en PowerShell
python3 scripts/fetch_destination_images.py
```

**Sortie :**
- `flask/app/static/images/destinations/<slug>-main.jpg`, `-thumb.jpg`, `-gallery-1/2/3.jpg`
- `database/seed/seed_images.sql` (à exécuter après `seed.sql`)

## fetch_gastronomy_culture_images.py

Complète le script précédent : récupère 1 photo par destination illustrant la gastronomie locale et 1 photo illustrant la culture/architecture, pour illustrer les onglets correspondants sur la page détail destination.

**Variable d'environnement requise :** `PEXELS_API_KEY` (même clé que ci-dessus).

**Commande (depuis la racine du projet) :**
```bash
export PEXELS_API_KEY=ta_cle
python3 scripts/fetch_gastronomy_culture_images.py
```

**Sortie :**
- `flask/app/static/images/destinations/<slug>-gastronomy.jpg`, `<slug>-culture.jpg`
- `database/seed/seed_gastronomy_culture.sql` (à exécuter après `seed.sql`)

## fetch_other_sections_images.py

Récupère une photo principale pour chaque hôtel, programme, article de blog, produit boutique et logo de compagnie aérienne (28 hôtels, 10 programmes, 4 articles, 5 produits, 8 compagnies).

**Variable d'environnement requise :** `PEXELS_API_KEY` (même clé que ci-dessus).

**Commande (depuis la racine du projet) :**
```bash
export PEXELS_API_KEY=ta_cle
python3 scripts/fetch_other_sections_images.py
```

**Sortie :**
- `flask/app/static/images/uploads/<slug>.jpg`
- `database/seed/seed_other_images.sql` (à exécuter après `seed.sql`)

Note : si le volume `uploads_data` est un volume Docker nommé (et non un bind mount), copier les fichiers téléchargés dans le conteneur après coup : `docker cp flask/app/static/images/uploads/. rtvoyage_flask:/app/app/static/images/uploads/`.
