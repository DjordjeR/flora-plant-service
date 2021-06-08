from sqlalchemy import Column, Integer, String, JSON
from ..database import Base


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    common_name = Column(String, nullable=False)
    latin_name = Column(String, nullable=False)
    metadata = Column(JSON, nullable=True)
