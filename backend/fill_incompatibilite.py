from PyPDF2 import PdfReader
from backend.models import Ingredient, Incompatibilite, db
from app import app
import re

def extract_incompatibilites(file_path):
    reader = PdfReader(file_path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    pattern = r"(\w[\w\s\(\)\+\-/']+)\s*\+\s*(\w[\w\s\(\)\+\-/']+)\n→\s*Risque\s*:\s*(.+)"
    incompat_list = re.findall(pattern, text)

    for ingA, ingB, raison in incompat_list:
        ingr1 = Ingredient.query.filter(Ingredient.nom.ilike(f"%{ingA.strip()}%")).first()
        ingr2 = Ingredient.query.filter(Ingredient.nom.ilike(f"%{ingB.strip()}%")).first()

        if ingr1 and ingr2:
            if not Incompatibilite.query.filter_by(ingredient_A=ingr1.id, ingredient_B=ingr2.id).first():
                incompat = Incompatibilite(
                    ingredient_A=ingr1.id,
                    ingredient_B=ingr2.id,
                    raison=raison.strip(),
                    source="PDF Incompatibilités"
                )
                db.session.add(incompat)

    db.session.commit()
    print(f"✅ {len(incompat_list)} incompatibilités ajoutées avec succès.")


if __name__ == "__main__":
    with app.app_context():
        extract_incompatibilites("ingredients_incompatibles.pdf")
