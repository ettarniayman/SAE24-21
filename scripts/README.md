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
