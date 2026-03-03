import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.models.base import Base
from app.models.user import User
from app.models.session import Session
from app.models.inscription import Inscription

from app.schemas.inscription import InscriptionCreate, InscriptionUpdate
from app.services.inscription_service import InscriptionService

@pytest.fixture
def db_session():
    """Fixture : crée une base SQLite en mémoire pour les tests."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(bind=engine)

    # Crée les tables dans la base en mémoire
    Base.metadata.create_all(engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_inscription(db_session):
    # Créer un utilisateur et une session pour lier l'inscription
    user = User(
        nom="Doe",
        prenom="John",
        email="john.doe@example.com",
        role="apprenant",
    )
    db_session.add(user)
    db_session.commit()

    session = Session(
        titre="Session de test",
        description="Description de la session de test",
        date=datetime(2023, 10, 1, 10, 0),
        duree=60,
    )
    db_session.add(session)
    db_session.commit()

    data = InscriptionCreate(
        user_id=user.id,
        session_id=session.id
    )

    new_inscription = InscriptionService.create(db_session, data)

    assert new_inscription.id is not None
    assert new_inscription.user_id == user.id
    assert new_inscription.session_id == session.id

def test_get_by_id(db_session):
    # Créer une inscription manuellement
    inscription = Inscription(
        user_id=1,
        session_id=1
    )
    db_session.add(inscription)
    db_session.commit()

    fetched = InscriptionService.get_by_id(db_session, inscription.id)

    assert fetched is not None
    assert fetched.user_id == 1
    assert fetched.session_id == 1

def test_get_all(db_session):
    # Créer plusieurs inscriptions manuellement
    for i in range(3):
        inscription = Inscription(
            user_id=i+1,
            session_id=i+1
        )
        db_session.add(inscription)
    db_session.commit()

    inscriptions = InscriptionService.get_all(db_session)

    assert len(inscriptions) == 3
    assert inscriptions[0].user_id == 1
    assert inscriptions[1].user_id == 2
    assert inscriptions[2].user_id == 3

def test_delete_inscription(db_session):
    inscription = Inscription(
        user_id=1,
        session_id=1
    )
    db_session.add(inscription)
    db_session.commit()

    result = InscriptionService.delete(db_session, inscription.id)

    assert result is not None
    assert result.id == inscription.id

    # Vérifier que l'inscription a été supprimée
    fetched = InscriptionService.get_by_id(db_session, inscription.id)
    assert fetched is None

def test_delete_inscription_not_found(db_session):
    result = InscriptionService.delete(db_session, 9999)
    assert result is None

