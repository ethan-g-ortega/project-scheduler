from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict

class ProjectStatus(str, Enum):
    PLANNED = 'planned'
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETE = "complete"

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