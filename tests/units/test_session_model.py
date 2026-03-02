import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.formation import Formation
from app.enums.level import Level

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


def test_create_session(db_session):
    formation = Formation(
        titre="Python Basics",
        description="Introduction au langage Python",
        duree=10,
        niveau=Level.debutant,
    )

    db_session.add(formation)
    db_session.commit()

    db_item = db_session.query(Formation).first()

    assert db_item is not None
    assert db_item.titre == "Python Basics"
    assert db_item.description == "Introduction au langage Python"
    assert db_item.duree == 10
    assert db_item.niveau == Level.debutant