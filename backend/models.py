from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

# --- Table Produit ---
class Produit(Base):
    __tablename__ = "produits"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, nullable=False)
    categorie = Column(String)
    composition = relationship("CompositionProduit", back_populates="produit")


# --- Table Ingrédient ---
class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, nullable=False)
    composition = relationship("CompositionProduit", back_populates="ingredient")


# --- Table de liaison Produit <-> Ingrédient ---
class CompositionProduit(Base):
    __tablename__ = "composition_produit"

    id = Column(Integer, primary_key=True, index=True)
    produit_id = Column(Integer, ForeignKey("produits.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))

    produit = relationship("Produit", back_populates="composition")
    ingredient = relationship("Ingredient", back_populates="composition")


# --- Table Incompatibilités ---
class Incompatibilite(Base):
    __tablename__ = "incompatibilites"

    id = Column(Integer, primary_key=True, index=True)
    ingredient_A = Column(Integer, ForeignKey("ingredients.id"))
    ingredient_B = Column(Integer, ForeignKey("ingredients.id"))
    raison = Column(String)
