from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text, func, Enum as SAEnum
from sqlalchemy.dialects.postgresql import CITEXT
from database import Base
import models
from enum import Enum
from schemas import ProjectStatus, PreferredLang


class Customers(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(CITEXT, nullable=False, unique=True)
    preferred_lang = Column(
        SAEnum(PreferredLang,
               name="preferred_lang_enum",
               native_enum=True,
               validate_strings=True,
               create_constraint=False,
               ),
               nullable=False,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


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