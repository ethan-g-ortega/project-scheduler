from sqlalchemy import Column, Integer, String, Float, DateTime, func, Enum as SAEnum
from sqlalchemy.dialects.postgresql import CITEXT
from app.db.session import Base

from app.schemas.customers import PreferredLang



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