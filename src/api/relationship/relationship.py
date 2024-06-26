from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from src.core.db.base import Base


class User(Base):

    requests = relationship("Request", back_populates="user")


class Request(Base):

    user = relationship("User", back_populates="requests")
    solutions = relationship("Solution", back_populates="request")


class Solution(Base):

    request_id = Column(Integer, ForeignKey("request.id"))
    request = relationship("Request", back_populates="solutions")