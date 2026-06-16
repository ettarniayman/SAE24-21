### RT Voyage — Agence de Voyage en Ligne

**"Explore the World Without Limits"**

Site web complet d'agence de voyage développé dans le cadre d'un projet SAE en Réseaux & Télécommunications.

## stack Technique

| Composant | Technologie |
|-----------|------------|
| Backend | Python 3.12 + Flask 3.1 |
| Base de données | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 + Alembic |
| Authentification | Flask-Login + bcrypt |
| Formulaires | Flask-WTF + CSRF |
| Serveur web | Apache 2.4 (reverse proxy) |
| Application server | Gunicorn |
| Infrastructure | Docker + Docker Compose |
| Frontend | HTML5 + CSS3 + JS (vanilla) |
| Cartes | Google Maps API + Street View |
| Graphiques | Chart.js |

## Fonctionnalités

- **80+ destinations** : Maroc (villes + nature), Europe, Asie, Amériques, Afrique
- **Programmes de voyage** avec itinéraires jour par jour
- **Football Experience** (Bernabéu, Camp Nou…)
- **Hôtels & Hébergements** (hôtels, riads, villas, resorts)
- **Compagnies aériennes partenaires** avec promotions vols
- **Boutique** (bagages, équipements, souvenirs)
- **Blog** avec catégories et fil RSS
- **Newsletter** avec confirmation par email
- **FAQ dynamique** par catégorie
- **Formulaire de contact** avec anti-spam (honeypot)
- **Panel admin complet** (rôles : super_admin, admin, agent, client)
- **Bilinguisme FR/EN** via cookie de session
- **SEO** : sitemap.xml, robots.txt, Open Graph, Schema.org
- **Dark Luxury Gold** — thème visuel premium exclusif

## Installation Rapide

### Prérequis
- Docker Desktop installé et démarré
- Git

### 1. Cloner le projet
```bash
git clone <repo-url> rtvoyage
cd rtvoyage
```

### 2. Configurer les variables d'environnement
```bash
cp .env.example .env
# Éditer .env et renseigner :
# - POSTGRES_PASSWORD
# - SECRET_KEY (clé aléatoire longue)
# - GOOGLE_MAPS_API_KEY (optionnel)
```

### 3. Démarrer les conteneurs
```bash
docker-compose up -d --build
```

### 4. Initialiser la base de données
```bash
# Attendre que PostgreSQL soit prêt (30s environ)
docker exec rtvoyage_flask flask db upgrade
docker exec -i rtvoyage_postgres psql -U rtvoyage -d rtvoyage_db < database/seed.sql
```

### 5. Accéder à l'application
| Service | URL |
|---------|-----|
| Site principal | http://localhost |
| Admin | http://localhost/admin |
| pgAdmin | http://localhost:5050 |

**Identifiants admin par défaut :**
- Email : `admin@rtvoyage.ma`
- Mot de passe : à définir dans `.env` ou via `flask create-admin`

## Structure du Projet

```
SAE24-21/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── database/
│   ├── schema.sql          # Schéma PostgreSQL complet
│   ├── seed.sql            # Données initiales (80+ destinations)
│   └── views_triggers.sql  # Vues et triggers
├── apache/
│   ├── Dockerfile
│   └── rtvoyage.conf       # VirtualHost + reverse proxy
└── flask/
    ├── Dockerfile
    ├── requirements.txt
    ├── wsgi.py
    ├── run.py
    ├── config.py
    └── app/
        ├── __init__.py     # Application factory
        ├── extensions.py   # SQLAlchemy, Login, CSRF…
        ├── models/         # Modèles ORM (15 fichiers)
        ├── routes/         # Blueprints (12 blueprints)
        ├── forms/          # Flask-WTF forms
        ├── utils/          # Helpers, upload, sanitize
        ├── static/
        │   ├── css/style.css
        │   └── js/
        │       ├── main.js
        │       ├── gallery.js
        │       ├── maps.js
        │       ├── admin.js
        │       ├── filters.js
        │       └── form-validation.js
        └── templates/
            ├── base.html
            ├── index.html
            ├── admin/
            ├── destinations/
            ├── programs/
            ├── hotels/
            ├── airlines/
            ├── blog/
            ├── shop/
            ├── auth/
            ├── pages/
            └── errors/
```

## Développement Local (sans Docker)

```bash
cd flask
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Créer la base PostgreSQL
createdb rtvoyage_db
psql rtvoyage_db < ../database/schema.sql
psql rtvoyage_db < ../database/seed.sql

# Variables d'environnement
set DATABASE_URL=postgresql://postgres:password@localhost/rtvoyage_db
set SECRET_KEY=votre-cle-secrete

# Migrations
flask db upgrade

# Lancer le serveur de dev
python run.py
```

## Variables d'Environnement

Voir `.env.example` pour la liste complète.

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Clé secrète Flask (générer avec `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `DATABASE_URL` | URL PostgreSQL |
| `GOOGLE_MAPS_API_KEY` | API Google Maps (optionnel) |
| `MAIL_SERVER` / `MAIL_USERNAME` | Configuration email |

## Thème Visual

**Dark Luxury Gold** — Design system premium :
- `--gold: #c9a96e` — or principal
- `--bg-deep: #050810` — fond profond
- Fonts : Cormorant Garamond (titres) + Montserrat (UI)
- Glassmorphism navbar + particules hero animées

## Licence

Projet académique SAE — Réseaux & Télécommunications.
