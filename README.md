# Simplon Training API

Une API RESTful développée avec FastAPI pour la gestion des formations de Simplon.

## 🚀 Fonctionnalités

- **Gestion des formations** : CRUD complet pour les formations
- **Système de niveaux** : Débutant, Intermédiaire, Avancé
- **Base de données** : SQLAlchemy avec PostgreSQL
- **Tests unitaires** : Pytest pour assurer la qualité du code
- **Documentation auto-générée** : Swagger/OpenAPI

## 📋 Prérequis

- Python 3.8+
- PostgreSQL
- pip ou poetry

## 🛠️ Installation

1. Cloner le repository :
```bash
git clone <repository-url>
cd BriefApi
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer la base de données :
   - Créer une base de données PostgreSQL
   - Configurer les variables d'environnement (voir section Configuration)

## ⚙️ Configuration

Créer un fichier `.env` à la racine du projet :

```env
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=votre-secret-key
```

## 🏃‍♂️ Lancement

Démarrer le serveur de développement :

```bash
uvicorn app.main:app --reload
```

L'API sera disponible sur `http://localhost:8000`

## 📚 Documentation

- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`

## 🔗 Endpoints

### Formations

- `GET /formations` - Lister toutes les formations
- `POST /formations` - Créer une nouvelle formation
- `GET /formations/{id}` - Obtenir une formation par son ID
- `PUT /formations/{id}` - Mettre à jour une formation
- `DELETE /formations/{id}` - Supprimer une formation

### Exemple de création de formation

```json
{
  "titre": "Python pour débutants",
  "description": "Apprendre les bases de la programmation Python",
  "duree": 40,
  "niveau": "débutant"
}
```

## 🧪 Tests

Lancer les tests unitaires :

```bash
pytest
```

Pour lancer les tests avec coverage :

```bash
pytest --cov=app
```

## 📁 Structure du projet

```
BriefApi/
├── app/
│   ├── database/          # Configuration de la base de données
│   ├── enums/            # Énumérations (niveaux, rôles)
│   ├── models/           # Modèles SQLAlchemy
│   ├── routers/          # Routes FastAPI
│   ├── schemas/          # Schémas Pydantic
│   ├── services/         # Logique métier
│   └── main.py           # Point d'entrée de l'application
├── tests/                # Tests unitaires
├── requirements.txt       # Dépendances Python
└── README.md            # Documentation du projet
```

## 🛠️ Technologies utilisées

- **FastAPI** : Framework web moderne et performant
- **SQLAlchemy** : ORM pour la base de données
- **Pydantic** : Validation des données
- **PostgreSQL** : Base de données relationnelle
- **Pytest** : Framework de tests
- **Uvicorn** : Serveur ASGI

## 🤝 Contributeurs

Projet réalisé dans le cadre de la formation Simplon.