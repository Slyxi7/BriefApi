from pydantic import BaseModel, ConfigDict
from typing import Optional

class SessionsFormateursCreate(BaseModel):
    session_id: int 
    formateur_id: int

class SessionsFormateursUpdate(BaseModel):
    session_id: Optional[int] = None
    formateur_id: Optional[int] = None

class SessionsFormateursRead(BaseModel):
    session_id: int 
    formateur_id: int
    model_config = ConfigDict(from_attributes=True)

class SessionsFormateursDelete(BaseModel):
    hard: bool = False