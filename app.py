from flask import Flask, render_template, request
from backend.database import SessionLocal
from backend.models import Produit, Ingredient, CompositionProduit, Incompatibilite
from backend.cosmetic_llm import extract_text_from_pdf, parse_pdf_text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyse', methods=['GET', 'POST'])
def analyse():
    result = None
    if request.method == 'POST':
        question = request.form.get('question')
        files = request.files.getlist('files')
        result = process_pdf_and_generate_text(files, question, save_to_db=True)
    return render_template('analyse.html', result=result)

@app.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    db = SessionLocal()
    produits = db.query(Produit).all()
    selected_produit = None
    ingredients = []
    if request.method == 'POST':
        produit_id = request.form.get('produit_id')
        selected_produit = db.query(Produit).get(produit_id)
        compositions = db.query(CompositionProduit).filter_by(produit_id=produit_id).all()
        ingredients = [db.query(Ingredient).get(c.ingredient_id) for c in compositions]
    db.close()
    return render_template('ingredients.html', produits=produits, selected_produit=selected_produit, ingredients=ingredients)

@app.route('/compatibilites', methods=['GET', 'POST'])
def compatibilites():
    db = SessionLocal()
    produits = db.query(Produit).all()
    result = None
    if request.method == 'POST':
        p1 = db.query(Produit).get(request.form.get('produit1'))
        p2 = db.query(Produit).get(request.form.get('produit2'))
        result = "Compatible ✅"
    db.close()
    return render_template('compatibilites.html', produits=produits, result=result)

if __name__ == "__main__":
    app.run(debug=True)
