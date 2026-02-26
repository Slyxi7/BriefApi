from sqlalchemy.orm import Session
from models.sessions_model import Sessions
from schemas.sessions_schema import (
    SessionsCreate,
    SessionsUpdate,
    SessionsRead,
    SessionsDelete
)


def get_sessions(db: Session):
    return db.query(Sessions).all()


def get_session_by_id(db: Session, session_id: int):
    return db.query(Sessions).filter(Sessions.id == session_id).first()


def create_session(db: Session, session: SessionsCreate):
    db_session = Sessions(**session.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def update_session(db: Session, session_db: Sessions, session_update: SessionsUpdate):
    update_data = session_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(session_db, key, value)

    db.commit()
    db.refresh(session_db)
    return session_db


def delete_session(db: Session, session_db: Sessions, delete_schema: SessionsDelete):
    # Hard delete (delete from DB)
    if delete_schema.hard:
        db.delete(session_db)

    # Soft delete (désactivation)  
    else:
        session_db.is_active = False

    db.commit()
    return {"detail": "Session supprimée" if delete_schema.hard else "Session désactivée"}