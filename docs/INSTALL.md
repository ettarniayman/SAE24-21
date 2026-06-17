# Guide d'installation detaille - RT Voyage

Ce guide complete la section "Installation Rapide" du [README.md](../README.md) avec le detail de chaque etape, les explications des variables d'environnement et les problemes courants.

## 1. Prerequis

| Outil | Version minimale | Verification |
|-------|-------------------|---------------|
| Docker Desktop | 24.x | `docker --version` |
| Docker Compose | v2 (integre a Docker Desktop) | `docker-compose --version` |
| Git | 2.x | `git --version` |

Sous Windows, Docker Desktop doit utiliser le backend WSL2 (active par defaut sur les installations recentes).

## 2. Cloner le projet

```bash
git clone <repo-url> rtvoyage
cd rtvoyage
```

## 3. Configurer les variables d'environnement

```bash
cp .env.example .env
```

Detail de chaque variable du `.env` :

| Variable | Role | A modifier en prod ? |
|----------|------|------------------------|
| `FLASK_ENV` | `development` active le mode debug Flask (rechargement auto, traces d'erreur completes). Mettre `production` en deploiement reel. | Oui |
| `SECRET_KEY` | Cle utilisee par Flask pour signer les sessions et jetons CSRF. Generer une valeur aleatoire avec `python -c "import secrets; print(secrets.token_hex(32))"`. | Oui, obligatoire |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | Identifiants de la base PostgreSQL, utilises a la fois par le conteneur `postgres` et par Flask pour s'y connecter. | Oui |
| `DATABASE_URL` | URL de connexion complete utilisee par SQLAlchemy. Doit rester coherente avec les 3 variables precedentes. | Oui |
| `GOOGLE_MAPS_API_KEY` | Cle API pour l'affichage des cartes sur les pages destination. Optionnelle : sans elle, les cartes ne s'affichent pas mais le site fonctionne. | Optionnel |
| `MAIL_SERVER` / `MAIL_PORT` / `MAIL_USERNAME` / `MAIL_PASSWORD` | Configuration SMTP pour l'envoi d'emails (confirmation newsletter, contact). Avec Gmail, `MAIL_PASSWORD` doit etre un mot de passe d'application, pas le mot de passe du compte. | Recommande |
| `PGADMIN_EMAIL` / `PGADMIN_PASSWORD` | Identifiants de connexion a l'interface pgAdmin (port 5050). | Recommande |
| `MAX_CONTENT_LENGTH` | Taille maximale en octets des fichiers uploadables (16 Mo par defaut). | Selon besoin |

## 4. Demarrer les conteneurs

```bash
docker-compose up -d --build
```

Cette commande construit et lance 4 conteneurs :

| Conteneur | Role | Port expose |
|-----------|------|--------------|
| `rtvoyage_postgres` | Base de donnees PostgreSQL 16 | 5432 |
| `rtvoyage_flask` | Application Flask via Gunicorn | interne (5000, via Apache) |
| `rtvoyage_apache` | Reverse proxy et serveur de fichiers statiques | 80, 443 |
| `rtvoyage_pgadmin` | Interface web d'administration PostgreSQL | 5050 |

Au premier demarrage, le conteneur `postgres` execute automatiquement, dans cet ordre, les scripts montes depuis `database/` :

1. `database/schema/schema.sql` (monte comme `01_schema.sql`) - cree toutes les tables
2. `database/schema/views_triggers.sql` (monte comme `02_views_triggers.sql`) - cree les vues et triggers
3. `database/seed/seed.sql` (monte comme `03_seed.sql`) - insere les donnees initiales (68 destinations, programmes, utilisateur admin, etc.)

Ces scripts ne s'executent qu'une seule fois, a la creation du volume `postgres_data`. Pour les rejouer (par exemple apres une modification de `seed.sql`), il faut detruire le volume :

```bash
docker-compose down -v
docker-compose up -d --build
```

`down -v` supprime aussi les donnees de pgAdmin et les fichiers uploades : a utiliser uniquement en developpement.

## 5. Appliquer les migrations Alembic

```bash
docker exec rtvoyage_flask flask db upgrade
```

Les migrations (`flask/migrations/versions/`) gerent les evolutions du schema posterieures a la version initiale de `schema.sql`. Cette commande est a relancer chaque fois qu'une nouvelle migration est ajoutee au projet.

## 6. Verifier que tout fonctionne

```bash
docker logs rtvoyage_postgres | grep -i error
docker logs rtvoyage_flask | tail -30
```

Aucune ligne ne devrait contenir d'erreur. Ouvrir ensuite :

| Service | URL |
|---------|-----|
| Site principal | http://localhost |
| Connexion / Admin | http://localhost/auth/connexion |
| pgAdmin | http://localhost:5050 |

**Compte administrateur par defaut** (defini dans `database/seed/seed.sql`) :
- Email : `admin@rtvoyage.ma`
- Mot de passe : `Admin@2025!`

A changer immediatement en production via le profil utilisateur ou directement en base.

## 7. Problemes courants

**`docker-compose up` echoue avec un port deja utilise**
Un autre service local occupe le port 80, 5432 ou 5050. Verifier avec `netstat -ano | findstr :80` (Windows) et arreter le processus concerne, ou modifier le port expose dans `docker-compose.yml`.

**`flask db upgrade` echoue avec `column ... already exists`**
Ne devrait plus se produire : les migrations historiques ont ete converties en no-op car leur contenu est deja present dans `schema.sql`. Si l'erreur reapparait apres l'ajout d'une nouvelle migration, verifier qu'elle n'essaie pas de recreer une colonne deja definie dans `schema.sql`.

**Le site repond mais sans styles ni images**
Verifier que le conteneur `rtvoyage_apache` est bien demarre (`docker ps`) et qu'il sert correctement `/static/` (monte depuis `flask/app/static`).

**Connexion admin impossible**
Verifier que `database/seed/seed.sql` a bien ete execute (regarder les logs postgres au premier demarrage) et que le volume n'a pas ete cree avant cette execution. En cas de doute, repartir d'un volume propre avec `docker-compose down -v`.

## 8. Developpement local sans Docker

Voir la section correspondante dans le [README.md](../README.md#développement-local-sans-docker). Cette approche necessite une instance PostgreSQL locale et l'execution manuelle des scripts SQL dans l'ordre schema puis vues/triggers puis seed.
