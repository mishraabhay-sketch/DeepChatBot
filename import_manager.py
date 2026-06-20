import os
import hashlib
import sqlite3
from pdf_import import extract_text as pdf_text
from docx_import import extract_text as docx_text
from txt_import import extract_text as txt_text
from excel_import import extract_text as excel_text
from image_import import extract_text as image_text
from database import (add_pdf_data,find_knowledge_by_question,update_knowledge, add_audit_log)
from utils import normalize_question
DB = "data/chatbot.db"
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

    elif ext in [
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp"
    ]:
        return image_text(path)
    return None

def import_any_file(file_path):

    file_hash = get_file_hash(file_path)
    filename = os.path.basename(file_path)
    
    if file_exists(file_hash):
        return "duplicate"

    text = import_file(file_path)

    if not text:
        return

    paragraphs = text.split("\n")

    for para in paragraphs:


        if ":" in para:

            parts = para.split(":", 1)

            question = parts[0].strip()
            
            # question = normalize_question(question)

            answer = parts[1].strip()

            existing = find_knowledge_by_question(question)

            if existing:

                knowledge_id = existing[0]
                old_answer = existing[1]

                if old_answer != answer:

                    update_knowledge(
                        knowledge_id,
                        answer,
                        filename
                    )

                    print(
                        "UPDATED:",
                        question
                    )

            else:

                add_pdf_data(
                    question,
                    answer,
                    filename
                )

                print(
                    "NEW:",
                    question
                )

        else:

            if len(para.split()) < 5:
                continue

            if para.isupper():
                continue

            if "handbook" in para.lower():
                continue

            if "chapter" in para.lower():
                continue

            if "index" in para.lower():
                continue
    
    save_imported_file(
        os.path.basename(file_path),
        file_hash
    )
    
    add_audit_log(
        "IMPORT FILE",
        "Founder",
        filename
    )
    print("File Imported Successfully")

def delete_file(file_id):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "SELECT filename FROM imported_files WHERE id=?",
        (file_id,)
    )

    row = cur.fetchone()

    if row:

        filename = row[0]

        cur.execute(
            "DELETE FROM knowledge WHERE source_file=?",
            (filename,)
        )

        cur.execute(
            "DELETE FROM imported_files WHERE id=?",
            (file_id,)
        )

    conn.commit()
    conn.close()



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


def delete_imported_file(file_name):

    print("DELETE REQUEST =", file_name)

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Knowledge delete
    cur.execute(
        """
        DELETE FROM knowledge
        WHERE source_file=?
        """,
        (file_name,)
    )

    print(
        "KNOWLEDGE DELETED =",
        cur.rowcount
    )

    # Imported file record delete
    cur.execute(
        """
        DELETE FROM imported_files
        WHERE file_name=?
        """,
        (file_name,)
    )

    print(
        "FILE RECORD DELETED =",
        cur.rowcount
    )

    conn.commit()
    conn.close()

    print("DELETE COMPLETE")


def get_imported_files():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT id, file_name
    FROM imported_files
    """)

    rows = cur.fetchall()

    conn.close()

    return rows
