from backend.database import Base, engine
from backend.models import Produit, Ingredient, CompositionProduit, Incompatibilite

def init_db():
    print("🧱 Création des tables dans la base de données...")
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données initialisée avec succès !")

if __name__ == "__main__":
    init_db()
