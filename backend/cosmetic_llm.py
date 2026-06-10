import os
import re
import fitz  # PyMuPDF pour lire les PDF
from backend.database import SessionLocal
from backend.models import Produit, Ingredient, CompositionProduit

# --- Extraire le texte d'un PDF ---
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text")
    return text


# --- Parser le texte du PDF pour identifier les produits et ingrédients ---
def parse_pdf_text(text):
    produits = []

    # On suppose que chaque produit commence par "Crème", "Gel", "Lotion", etc.
    blocs = re.split(r"\n(?=\d+\.)", text.strip())
    for bloc in blocs:
        lignes = bloc.strip().split("\n")
        if not lignes:
            continue

        nom = lignes[0].strip()
        ingredients = []

        for ligne in lignes:
            if "Ingrédients" in ligne or "Ingredients" in ligne:
                # Extraction entre `:` et fin
                ing_text = ligne.split(":")[-1]
                ingredients = [i.strip() for i in re.split(r",|;", ing_text) if i.strip()]

        if nom:
            produits.append({"nom": nom, "ingredients": ingredients})
    return produits


# --- Enregistrer les produits et ingrédients dans la base ---
def save_to_database(produits):
    db = SessionLocal()

    for p in produits:
        produit = Produit(nom=p["nom"], categorie="Inconnue")
        db.add(produit)
        db.commit()
        db.refresh(produit)

        for nom_ing in p["ingredients"]:
            ingredient = db.query(Ingredient).filter_by(nom=nom_ing).first()
            if not ingredient:
                ingredient = Ingredient(nom=nom_ing)
                db.add(ingredient)
                db.commit()
                db.refresh(ingredient)

            association = CompositionProduit(produit_id=produit.id, ingredient_id=ingredient.id)
            db.add(association)

    db.commit()
    db.close()
    print("✅ Données insérées avec succès !")


# --- Lire tous les PDF dans le dossier /data et les insérer dans la base ---
def process_all_pdfs():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    for file in os.listdir(data_dir):
        if file.endswith(".pdf"):
            path = os.path.join(data_dir, file)
            print(f"📄 Lecture de {file} ...")
            text = extract_text_from_pdf(path)
            produits = parse_pdf_text(text)
            save_to_database(produits)

    print("🎉 Tous les fichiers PDF ont été traités !")


if __name__ == "__main__":
    process_all_pdfs()
