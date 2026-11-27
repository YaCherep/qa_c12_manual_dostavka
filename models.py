from pydantic import BaseModel
from typing import Optional 

class CourierModel(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    phone: Optional[str] = None