from flask import current_app
from backend.models import db, Produit, Ingredient, CompositionProduit
import logging

def save_product_from_pdf(nom, categorie, marque, description, ingredients):
    """Ajoute un produit et ses ingrédients dans la base SQLite."""
    try:
        # On s'assure d'être dans le contexte de l'application Flask
        with current_app.app_context():
            produit = Produit(
                nom=nom,
                categorie=categorie,
                marque=marque,
                description=description
            )
            db.session.add(produit)
            db.session.commit()

            for ing in ingredients:
                ingredient = Ingredient.query.filter_by(nom=ing["nom"]).first()
                if not ingredient:
                    ingredient = Ingredient(
                        nom=ing["nom"],
                        fonction=ing.get("fonction", ""),
                        risque=ing.get("risque", "")
                    )
                    db.session.add(ingredient)
                    db.session.commit()

                comp = CompositionProduit(
                    produit_id=produit.id,
                    ingredient_id=ingredient.id,
                    quantite=ing.get("quantite", "")
                )
                db.session.add(comp)

            db.session.commit()
            logging.info(f"✅ Produit '{nom}' ajouté avec succès avec {len(ingredients)} ingrédients.")

    except Exception as e:
        db.session.rollback()
        logging.error(f"❌ Erreur ajout produit : {e}")
