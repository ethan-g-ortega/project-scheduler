from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Text, func, Enum as SAEnum
from app.db.session import Base
from app.schemas.projects import ProjectStatus



class Projects(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False) #foreign key will link back to customer 
    address_line = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state_region = Column(String(255), nullable=False)
    postal_code = Column(String(15), nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    start_date = Column(DateTime(timezone=True))
    eta_date = Column(DateTime(timezone=True))
    status = Column(
        SAEnum(
            ProjectStatus,
            name="project_status_enum",
            native_enum=True,
            validate_strings=True,
        ),
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = Column(Text)