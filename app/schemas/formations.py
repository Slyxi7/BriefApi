from pydantic import BaseModel, field_validator

NIVEAU = ["débutant", "intermédiaire", "avancé"]

class FormationBase(BaseModel):
    titre: str
    description: str | None = None
    duree: int
    niveau: str
   
    @field_validator("niveau")
    def validate_niveau(cls, val):
        if val not in NIVEAU:
            raise ValueError(f"Niveau invalide. Choisir parmi : {NIVEAU}")
        return val

    @field_validator("duree")
    def validate_duree(cls, val):
        if val <= 0:
            raise ValueError("La durée doit être > 0")
        return val

class FormationCreate(FormationBase):
    pass

class FormationUpdate(FormationBase):
    titre: str | None = None
    description: str | None = None
    duree: int | None = None
    niveau: str | None = None
   
    @field_validator("niveau")
    def validate_niveau(cls, val):   
        if val is None:
            return val
        if val not in NIVEAU:
            raise ValueError(f"Niveau invalide. Choisir parmi : {NIVEAU}")
        return val

    @field_validator("duree")
    def validate_duree(cls, val):
        if val is None:
            return val
        if val <= 0:
            raise ValueError("La durée doit être > 0")
        return val

class InscriptionRead(FormationBase):
    id: int

    class Config: from_attributes = True

class InscriptionDelete(BaseModel):
    hard: bool = False