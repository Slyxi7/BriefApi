from pydantic import BaseModel, ConfigDict
from typing import Optional

class SessionsFormateursBase(BaseModel):
    session_id: int 
    formateur_id: int


class SessionsFormateursCreate(SessionsFormateursBase):
    pass

class SessionsFormateursUpdate(SessionsFormateursBase):
    session_id: Optional[int] = None
    formateur_id: Optional[int] = None

class SessionsFormateursRead(SessionsFormateursBase):
    model_config = ConfigDict(from_attributes=True)

class SessionsFormateursDelete(BaseModel):
    hard: bool = False