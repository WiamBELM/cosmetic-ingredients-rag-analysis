import os
from backend.cosmetic_llm import process_pdf_and_generate_text

def fill_database_from_pdfs():
    folder = "data"
    pdfs = [open(os.path.join(folder, f), 'rb') for f in os.listdir(folder) if f.endswith('.pdf')]
    process_pdf_and_generate_text(pdfs, save_to_db=True)

if __name__ == "__main__":
    fill_database_from_pdfs()
