from datetime import datetime

from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.core.db.base import Base


class Solution(Base):
    __tablename__ = "solution"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    response_at = Column(DateTime, default=datetime)
    request_id = Column(Integer, ForeignKey("request.id"))

    requests = relationship("Request", back_populates="solution")
