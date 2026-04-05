from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Championship(Base):
    __tablename__ = "championships"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    matches = relationship("Match", back_populates="championship", cascade="all, delete-orphan")

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    championship_id = Column(Integer, ForeignKey("championships.id"), nullable=False)
    category = Column(String, nullable=False) # Ex: "Dupla Mista", "Dupla Masculina"
    stage = Column(String, nullable=False)    # Ex: "Fase de Grupos", "Quartos de Final"
    our_score = Column(Integer, nullable=False) # Placar em sets (Ex: 2 x 1)
    opponent_score = Column(Integer, nullable=False) 
    partner = Column(String, nullable=True) # Fica nulo se for Simples
    opponents = Column(String, nullable=True)
    championship = relationship("Championship", back_populates="matches")
    sets = relationship("MatchSet", back_populates="match", cascade="all, delete-orphan")

class MatchSet(Base):
    __tablename__ = "match_sets"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    our_points = Column(Integer, nullable=False) # Pontuação de cada set
    opponent_points = Column(Integer, nullable=False)
    match = relationship("Match", back_populates="sets")