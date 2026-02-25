from pydantic import BaseModel, ConfigDict

class SessionsFormateursBase(BaseModel):
    session_id: int 
    formateur_id: int


class SessionsFormateursCreate(SessionsFormateursBase):
    pass

class SessionsFormateursUpdate(SessionsFormateursBase):
    session_id: int | None = None 
    formateur_id: int | None = None 

class SessionsFormateursRead(SessionsFormateursBase):
    model_config = ConfigDict(from_attributes=True)

class SessionsFormateursDelete(BaseModel):
    hard: bool = False