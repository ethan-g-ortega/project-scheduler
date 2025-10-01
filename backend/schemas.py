
from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict

class PreferredLang(str, Enum):
    EN = "en"
    ES = "es"

class ProjectStatus(str, Enum):
    PLANNED = 'planned'
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETE = "complete"

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

class ProjectBase(BaseModel):
   
    address_line: str
    city: str
    state_region: str
    postal_code: str
    lat: float
    lon: float
    start_date: Optional[datetime] = None
    eta_date: Optional[datetime] = None
    status: ProjectStatus = ProjectStatus.PLANNED
    model_config = ConfigDict(use_enum_values=True)  # <- ensures 'planned', 'in_progress', etc. in payloads
    notes: Optional[str] = None

class ProjectCreate(ProjectBase):
    customer_id: int
    pass

class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ProjectUpdate(ProjectBase):
    address_line: Optional[str] = None
    city: Optional[str] = None
    state_region: Optional[str] = None
    postal_code: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    start_date: Optional[datetime] = None
    eta_date: Optional[datetime] = None
    status: Optional[ProjectStatus] = None
    notes: Optional[str] = None
    