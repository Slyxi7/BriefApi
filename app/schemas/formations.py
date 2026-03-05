from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
from app.enums.level import Level

class FormationCreate(BaseModel):
    titre: str
    description: str | None = None
    duree: int
    niveau: Level

    @field_validator("duree")
    def validate_duree(cls, val):
        if val <= 0:
            raise ValueError("Duration must be greater than 0")
        return val

class FormationUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    duree: Optional[int] = None
    niveau: Optional[Level] = None

    @field_validator("duree")
    def validate_duree(cls, val):
        if val is None:
            return val
        if val <= 0:
            raise ValueError("Duration must be greater than 0")
        return val

class FormationRead(BaseModel):
    id: int
    titre: str
    description: str | None = None
    duree: int
    niveau: Level

    model_config = ConfigDict(from_attributes=True)

class FormationDelete(BaseModel):
    hard: bool = False