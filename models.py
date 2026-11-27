from pydantic import BaseModel
from typing import Optional 

class CourierModel(BaseModel):
    id: int
    first_name: str
    phone: Optional[str] = None