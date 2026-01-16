from docx import Document
from datetime import date
from services import member_service
import os

TEMPLATE_PATH = "templates/ricevuta.docx"
OUTPUT_DIR = "output/ricevute"

def generate_receipt(member_id, start, end):
    doc = Document(TEMPLATE_PATH)

    member=member_service.get_member_by_id(member_id)

    replacements = {
        "{{NOME}}": member["nome"],
        "{{COGNOME}}": member["cognome"],
        "{{DATA_INIZIO}}": start,
        "{{DATA_FINE}}": end,
        "{{CODICE_FISCALE}}":member["codice_fiscale"],
        "{{LUOGO_NASCITA}}":member["luogo_nascita"],
        "{{DATA_NASCITA}}":member["data_nascita"]        

    }

    for p in doc.paragraphs:
        for k, v in replacements.items():
            if k in p.text:
                p.text = p.text.replace(k, v)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"ricevuta_{member['cognome']}_{date.today()}.docx"
    path = os.path.join(OUTPUT_DIR, filename)

    doc.save(path)
    os.startfile(path)  # apre il file
