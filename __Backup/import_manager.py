import os
import hashlib
import sqlite3
from pdf_import import extract_text as pdf_text
from docx_import import extract_text as docx_text
from txt_import import extract_text as txt_text
from excel_import import extract_text as excel_text

from database import add_pdf_data

def import_file(path):

    ext = os.path.splitext(
        path
    )[1].lower()

    if ext == ".pdf":
        return pdf_text(path)

    elif ext == ".docx":
        return docx_text(path)

    elif ext == ".txt":
        return txt_text(path)

    elif ext == ".xlsx":
        return excel_text(path)

    return None

def import_any_file(file_path):

    file_hash = get_file_hash(file_path)

    if file_exists(file_hash):
        return "duplicate"

    text = import_file(file_path)

    if not text:
        return

    paragraphs = text.split("\n")

    for para in paragraphs:

        para = para.strip()

        if len(para) > 20:

            add_pdf_data(
                para[:100],
                para
            )
    save_imported_file(
        os.path.basename(file_path),
        file_hash
    )
    
    print("File Imported Successfully")

def get_file_hash(file_path):

    hasher = hashlib.md5()

    with open(file_path, "rb") as f:

        while chunk := f.read(4096):

            hasher.update(chunk)

    return hasher.hexdigest()

def file_exists(file_hash):

    conn = sqlite3.connect(
        "data/chatbot.db"
    )

    cur = conn.cursor()

    cur.execute(
        """
        SELECT id
        FROM imported_files
        WHERE file_hash=?
        """,
        (file_hash,)
    )

    result = cur.fetchone()

    conn.close()

    return result is not None

def save_imported_file(
    file_name,
    file_hash
):

    conn = sqlite3.connect(
        "data/chatbot.db"
    )

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO imported_files(
            file_name,
            file_hash
        )
        VALUES (?,?)
        """,
        (
            file_name,
            file_hash
        )
    )

    conn.commit()
    conn.close()

