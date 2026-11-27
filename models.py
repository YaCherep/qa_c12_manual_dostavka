from pydantic import BaseModel
from typing import Optional 

class CourierModel(BaseModel):
    model_config = ConfigDict(extra='ignore') 
    
    id: int
    first_name: str
    phone: Optional[str] = None