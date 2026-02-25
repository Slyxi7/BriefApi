from pydantic import BaseModel, field_validator
from typing import Optional
from enums.level import Level

class FormationBase(BaseModel):
    titre: str
    description: str | None = None
    duree: int
    niveau: Level
   
    @field_validator("niveau")
    def validate_niveau(cls, val):
        if val not in Level:
            raise ValueError(f"Niveau invalide. Choisir parmi : {Level}")
        return val

    @field_validator("duree")
    def validate_duree(cls, val):
        if val <= 0:
            raise ValueError("La durée doit être > 0")
        return val

class FormationCreate(FormationBase):
    pass

class FormationUpdate(FormationBase):
    titre: Optional[str] = None
    description: Optional[str] = None
    duree: Optional[int] = None
    niveau: Optional[Level] = None
   
    @field_validator("niveau")
    def validate_niveau(cls, val):   
        if val not in Level:
            raise ValueError(f"Niveau invalide. Choisir parmi : {Level}")
        return val

    @field_validator("duree")
    def validate_duree(cls, val):
        if val <= 0:
            raise ValueError("La durée doit être > 0")
        return val

class InscriptionRead(FormationBase):
    id: int

    class Config: from_attributes = True

class InscriptionDelete(BaseModel):
    hard: bool = False