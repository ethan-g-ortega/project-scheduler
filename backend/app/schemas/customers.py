from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict


class PreferredLang(str, Enum):
    EN = "en"
    ES = "es"

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    preferred_lang: PreferredLang

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name:  Optional[str] = None
    email: Optional[EmailStr] = None
    preferred_lang: Optional[PreferredLang] = None