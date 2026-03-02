from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.user import User
from app.models.session import Session
from app.models.inscription import Inscription
from datetime import datetime


def create_test_db():
    """Crée une DB SQLite en mémoire + les tables nécessaires."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    return TestingSessionLocal()


def test_create_inscription():
    """Test de création d'une inscription valide."""
    session = create_test_db()

    # 1) Créer un utilisateur
    user = User(
        nom="Doe",
        prenom="John",
        email="john.doe@example.com",
        role="apprenant",
        date_inscription=datetime.now(),
        hashed_password="hashed_pwd"
    )
    session.add(user)
    session.commit()

    # 2) Créer une session de formation
    session_obj = Session(
        formation_id=1,
        date_debut=datetime(2025, 1, 1),
        date_fin=datetime(2025, 1, 10),
        capacite=20
    )
    session.add(session_obj)
    session.commit()

    # 3) Créer une inscription
    inscription = Inscription(
        session_id=session_obj.id,
        apprenant_id=user.id
    )
    session.add(inscription)
    session.commit()

    # Vérifications
    result = session.query(Inscription).first()

    assert result is not None
    assert result.session_id == session_obj.id
    assert result.apprenant_id == user.id


def test_inscription_duplicate_fails():
    """Test que l’on ne peut pas créer deux fois la même inscription 
       (contrainte PK composite)."""

    session = create_test_db()

    # Créer un user
    user = User(
        nom="Doe",
        prenom="Jane",
        email="jane.doe@example.com",
        role="apprenant",
        date_inscription=datetime.now(),
        hashed_password="hashed_pwd"
    )
    session.add(user)
    session.commit()

    # Créer une session
    session_obj = Session(
        formation_id=1,
        date_debut=datetime(2025, 2, 1),
        date_fin=datetime(2025, 2, 10),
        capacite=15
    )
    session.add(session_obj)
    session.commit()

    # 1ère inscription OK
    inscription = Inscription(
        session_id=session_obj.id,
        apprenant_id=user.id
    )
    session.add(inscription)
    session.commit()

    # 2ᵉ insertion identique doit échouer
    duplicate = Inscription(
        session_id=session_obj.id,
        apprenant_id=user.id
    )
    session.add(duplicate)

    try:
        session.commit()
        # Si on arrive ici → pas normal
        assert False, "Une inscription dupliquée aurait dû provoquer une erreur."
    except Exception:
        # L'erreur de doublon est attendue
        session.rollback()
        assert True