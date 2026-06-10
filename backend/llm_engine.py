import sqlite3

def ask_cosmetiq_ai(question, db_path):
    question = question.lower()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 🔍 Recherche par mot-clé dans la base
    if "produit" in question:
        cur.execute("SELECT nom, description FROM produit")
        produits = cur.fetchall()
        if produits:
            reponse = "🌸 Voici les produits disponibles :\n\n"
            for nom, desc in produits:
                reponse += f"💄 **{nom}** — {desc}\n"
        else:
            reponse = "Aucun produit enregistré."
    
    elif "ingrédient" in question or "ingredient" in question:
        cur.execute("SELECT nom, risque FROM ingredient")
        ingredients = cur.fetchall()
        reponse = "🧴 Liste des ingrédients et leurs risques :\n\n"
        for nom, risque in ingredients:
            reponse += f"• {nom} : {risque}\n"

    elif "incompatibilité" in question or "incompatible" in question:
        cur.execute("""
            SELECT i1.nom, i2.nom, inc.raison
            FROM incompatibilite inc
            JOIN ingredient i1 ON inc.ingredient_A = i1.id
            JOIN ingredient i2 ON inc.ingredient_B = i2.id
        """)
        data = cur.fetchall()
        reponse = "⚠️ Ingrédients incompatibles détectés :\n\n"
        for a, b, raison in data:
            reponse += f"❌ {a} + {b} → {raison}\n"
    
    else:
        reponse = (
            "💬 Je peux vous donner des informations sur les produits, ingrédients "
            "et leurs incompatibilités. Par exemple :\n"
            "- 'Montre-moi les produits'\n"
            "- 'Quels ingrédients sont risqués ?'\n"
            "- 'Y a-t-il une incompatibilité entre la vitamine C et le rétinol ?'"
        )

    conn.close()
    return reponse
