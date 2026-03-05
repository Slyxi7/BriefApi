# Simplon Training API

API REST développée avec FastAPI pour la gestion des formations dans un
environnement de formation type Simplon.

Cette API permet de gérer les formations, les utilisateurs, les sessions
et les inscriptions via une architecture backend claire basée sur
FastAPI, SQLAlchemy, Pydantic et Alembic.

------------------------------------------------------------------------

# Fonctionnalités

-   Gestion des utilisateurs
-   Gestion des formations
-   Gestion des sessions de formation
-   Gestion des inscriptions aux sessions
-   Validation des données avec Pydantic
-   Documentation automatique de l'API avec Swagger et OpenAPI
-   Migrations de base de données avec Alembic
-   Tests unitaires avec Pytest

------------------------------------------------------------------------

# Technologies utilisées

-   FastAPI
-   SQLAlchemy
-   Pydantic
-   PostgreSQL
-   Alembic
-   Pytest
-   Uvicorn

------------------------------------------------------------------------

# Prérequis

-   Python 3.10 ou version supérieure
-   PostgreSQL
-   pip

------------------------------------------------------------------------

# Installation

## Cloner le repository

``` bash
git clone <repository-url>
cd BriefApi
```

## Créer un environnement virtuel

Linux / Mac :

``` bash
python -m venv venv
source venv/bin/activate
```

Windows :

``` bash
python -m venv venv
venv\Scripts\activate
```

## Installer les dépendances

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# Configuration

Créer un fichier `.env` à la racine du projet :

    DATABASE_URL=postgresql://username:password@localhost/briefapi
    SECRET_KEY=votre-secret-key

Créer ensuite une base PostgreSQL correspondant à l'URL configurée.

------------------------------------------------------------------------

# Migrations de base de données

Le projet utilise Alembic pour gérer les migrations.

## Appliquer les migrations

``` bash
alembic upgrade head
```

Cette commande crée les tables dans la base de données.

## Créer une migration après modification d'un modèle

``` bash
alembic revision --autogenerate -m "description de la migration"
```

Puis appliquer la migration :

``` bash
alembic upgrade head
```

## Vérifier la version actuelle

``` bash
alembic current
```

## Revenir à une migration précédente

``` bash
alembic downgrade -1
```

------------------------------------------------------------------------

# Lancement de l'application

Démarrer le serveur de développement :

``` bash
uvicorn app.main:app --reload
```

L'API sera accessible à l'adresse :

    http://localhost:8000

------------------------------------------------------------------------

# Documentation de l'API

Swagger UI :

    http://localhost:8000/docs

ReDoc :

    http://localhost:8000/redoc

------------------------------------------------------------------------

# Endpoints principaux

## Utilisateurs

  Méthode   Endpoint      Description
  --------- ------------- ---------------------------
  GET       /users        Liste les utilisateurs
  POST      /users        Crée un utilisateur
  GET       /users/{id}   Récupère un utilisateur
  PATCH     /users/{id}   Met à jour un utilisateur
  DELETE    /users/{id}   Supprime un utilisateur

## Formations

  Méthode   Endpoint           Description
  --------- ------------------ -----------------------------
  GET       /formations        Liste toutes les formations
  POST      /formations        Crée une formation
  GET       /formations/{id}   Récupère une formation
  PUT       /formations/{id}   Met à jour une formation
  DELETE    /formations/{id}   Supprime une formation

## Sessions

  Méthode   Endpoint         Description
  --------- ---------------- ----------------------
  GET       /sessions        Liste les sessions
  POST      /sessions        Crée une session
  GET       /sessions/{id}   Récupère une session

## Inscriptions

  -------------------------------------------------------------------------------------------
  Méthode                 Endpoint                                    Description
  ----------------------- ------------------------------------------- -----------------------
  POST                    /inscriptions                               Inscrit un utilisateur
                                                                      à une session

  DELETE                  /inscriptions/{session_id}/{apprenant_id}   Désinscrit un
                                                                      utilisateur

  GET                     /inscriptions/session/{id}                  Liste les inscrits à
                                                                      une session
  -------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Exemple de requête

Création d'une formation :

``` json
{
  "titre": "Python pour débutants",
  "description": "Apprendre les bases de la programmation Python",
  "duree": 40,
  "niveau": "debutant"
}
```

------------------------------------------------------------------------

# Tests

Lancer les tests :

``` bash
pytest
```

Lancer les tests avec couverture :

``` bash
pytest --cov=app
```

------------------------------------------------------------------------

# Structure du projet

    BriefApi/
    │
    ├── app/
    │   ├── database/
    │   ├── enums/
    │   ├── models/
    │   ├── schemas/
    │   ├── routers/
    │   ├── services/
    │   └── main.py
    │
    ├── alembic/
    │
    ├── tests/
    │
    ├── requirements.txt
    │
    └── README.md