import sqlite3
import numpy as np
import pickle
import tempfile
import os
from datetime import datetime

DB_NAME = "missing_person.db"


# -------------------------
# CREATE TABLES
# -------------------------
def create_tables():

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Missing persons
    c.execute("""
    CREATE TABLE IF NOT EXISTS missing_persons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        aadhar TEXT,
        last_seen TEXT,
        date_missing TEXT,
        description TEXT,
        contact TEXT,
        image BLOB,
        embedding BLOB
    )
    """)

    # Found persons
    c.execute("""
    CREATE TABLE IF NOT EXISTS already_found (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        aadhar TEXT,
        last_seen TEXT,
        contact TEXT,
        missing_image BLOB,
        found_image BLOB,
        found_latitude REAL,
        found_longitude REAL,
        found_date TEXT
    )
    """)

    conn.commit()
    conn.close()


# -------------------------
# GET EMBEDDING
# -------------------------
def get_embedding(img_path):

    from deepface import DeepFace

    rep = DeepFace.represent(
        img_path,
        model_name="Facenet512",
        detector_backend="opencv",
        enforce_detection=False,
        align=True
    )

    emb = np.array(rep[0]["embedding"])
    emb = emb / np.linalg.norm(emb)

    return emb


# -------------------------
# INSERT MISSING PERSON
# -------------------------
def insert_missing_person(name, age, gender, aadhar,
                          last_seen, date_missing,
                          description, contact, photo):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
        temp.write(photo.getvalue())
        img_path = temp.name

    try:
        embedding = get_embedding(img_path)
        embedding_blob = pickle.dumps(embedding)
        os.remove(img_path)

    except:
        return False

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO missing_persons
    (name, age, gender, aadhar, last_seen,
     date_missing, description, contact,
     image, embedding)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        name, age, gender, aadhar,
        last_seen, str(date_missing),
        description, contact,
        photo.getvalue(), embedding_blob
    ))

    conn.commit()
    conn.close()

    return True


# -------------------------
# MATCH FACE
# -------------------------
def match_face(photo):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
        temp.write(photo.getvalue())
        img_path = temp.name

    try:
        uploaded_embedding = get_embedding(img_path)
        os.remove(img_path)

    except:
        return None

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    SELECT name, age, aadhar,
           last_seen, contact,
           image, embedding
    FROM missing_persons
    """)

    rows = c.fetchall()
    conn.close()

    best_match = None
    best_similarity = -1

    for row in rows:

        db_embedding = pickle.loads(row[6])
        similarity = np.dot(uploaded_embedding, db_embedding)

        if similarity > 0.55 and similarity > best_similarity:

            best_similarity = similarity

            best_match = {
                "Name": row[0],
                "Age": row[1],
                "Aadhar": row[2],
                "Last Seen": row[3],
                "Contact": row[4],
                "Image": row[5],
                "Confidence": int(similarity * 100)
            }

    return best_match


# -------------------------
# SAVE FOUND MATCH
# -------------------------
def save_found_match(result, uploaded_photo, lat, lon):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    SELECT id FROM already_found
    WHERE name=? AND aadhar=?
    """, (result["Name"], result["Aadhar"]))

    exists = c.fetchone()

    if exists:
        conn.close()
        return False

    c.execute("""
    INSERT INTO already_found
    (name, age, aadhar, last_seen,
     contact, missing_image,
     found_image, found_latitude,
     found_longitude, found_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        result["Name"],
        result["Age"],
        result["Aadhar"],
        result["Last Seen"],
        result["Contact"],
        result["Image"],
        uploaded_photo.getvalue(),
        lat,
        lon,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    conn.commit()
    conn.close()

    return True