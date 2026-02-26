from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class SessionsCreate(BaseModel):
    formation_id: int 
    date_debut: datetime
    date_fin: datetime
    capacite: int

    @field_validator("capacite")
    def validate_capacite(cls, val):
        if val <= 0:
            raise ValueError("La capacité doit être > 0")
        return val

    @field_validator("date_fin")
    def validate_date(cls, val, info):
        if val <= info.data.get("date_debut"):
            raise ValueError("La capacité doit être > 0")
        return val

class SessionsUpdate(BaseModel):
    formation_id: Optional[int] = None
    date_debut: Optional[datetime] = None
    date_fin: Optional[datetime] = None
    capacite: Optional[int] = None


    @field_validator("capacite")
    def validate_capacite(cls, val):

        if val <= 0:
            raise ValueError("La capacité doit être > 0")
        return val

    @field_validator("date_fin")
    def validate_date(cls, val, info):
        if val is None:
            return val
        if val <= info.data.get("date_debut"):
            raise ValueError("La capacité doit être > 0")
        return val
    
class SessionsRead(BaseModel):
    id: int
    formation_id: int 
    date_debut: datetime
    date_fin: datetime
    capacite: int

    model_config = ConfigDict(from_attributes=True)

class SessionsDelete(BaseModel):
    hard: bool = False