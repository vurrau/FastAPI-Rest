from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from src.api.user.model import User
from src.api.request.model import Request
from src.api.solution.model import Solution
from src.core.db.base import Base


class User(Base):

    requests = relationship("Request", back_populates="user")


class Request(Base):

    user = relationship("User", back_populates="requests")
    solutions = relationship("Solution", back_populates="request")


class Solution(Base):

    request_id = Column(Integer, ForeignKey("request.id"))
    request = relationship("Request", back_populates="solutions")