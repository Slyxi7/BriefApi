import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.formation import Formation
from app.schemas.formations import FormationCreate, FormationUpdate
from app.services.formation_service import FormationService
from app.enums.level import Level


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_formation(db_session):
    data = FormationCreate(
        titre="Formation Python",
        description="Apprendre Python",
        duree=40,
        niveau=Level.debutant
    )

    new_f = FormationService.create(db_session, data)

    assert new_f.id is not None
    assert new_f.titre == "Formation Python"
    assert new_f.description == "Apprendre Python"
    assert new_f.duree == 40
    assert new_f.niveau == Level.debutant


def test_get_by_id(db_session):
    # Insert manually
    f = Formation(
        titre="Test SQL",
        description="desc",
        duree=20,
        niveau=Level.intermediaire,
    )
    db_session.add(f)
    db_session.commit()

    fetched = FormationService.get_by_id(db_session, f.id)

    assert fetched is not None
    assert fetched.titre == "Test SQL"
    assert fetched.niveau == Level.intermediaire


def test_get_all(db_session):
    f1 = Formation(
        titre="F1",
        description="desc",
        duree=10,
        niveau=Level.debutant,
    )
    f2 = Formation(
        titre="F2",
        description="desc2",
        duree=20,
        niveau=Level.avance,
    )
    db_session.add_all([f1, f2])
    db_session.commit()

    formations = FormationService.get_all(db_session)

    assert len(formations) == 2
    assert formations[0].titre == "F1"
    assert formations[1].titre == "F2"


def test_update_formation(db_session):
    f = Formation(
        titre="Old",
        description="Old desc",
        duree=15,
        niveau=Level.debutant,
    )
    db_session.add(f)
    db_session.commit()

    update_data = FormationUpdate(
        titre="New Title",
        duree=30,
    )

    updated = FormationService.update(db_session, f.id, update_data)

    assert updated is not None
    assert updated.titre == "New Title"
    assert updated.duree == 30
    assert updated.description == "Old desc"  # unchanged
    assert updated.niveau == Level.debutant  # unchanged


def test_update_formation_not_found(db_session):
    update_data = FormationUpdate(
        titre="Does not matter"
    )

    result = FormationService.update(db_session, 9999, update_data)

    assert result is None


def test_delete_formation(db_session):
    f = Formation(
        titre="To Delete",
        description="Temp",
        duree=10,
        niveau=Level.debutant,
    )
    db_session.add(f)
    db_session.commit()

    result = FormationService.delete(db_session, f.id)

    assert result is True
    assert FormationService.get_by_id(db_session, f.id) is None


def test_delete_formation_not_found(db_session):
    result = FormationService.delete(db_session, 9999)
    assert result is None