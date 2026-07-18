from pydantic import BaseModel

#   Define the model for validation
class User(BaseModel):
    id: int
    name:str
    surname:str
    idNo:str
    dob:str