from pydantic import BaseModel
from datetime import date

#   Define the model for validation
class User(BaseModel):
    id: int
    name:str
    surname:str
    idNo:str    
    dob:date