import streamlit as st
import sqlite3
from PIL import Image
import io

st.set_page_config(page_title="Active Cases")
st.title("Active Cases")

DB_NAME = "missing_person.db"

# ---------- SEARCH ----------
st.subheader("Filters")

search_name = st.text_input("Search by Name")
search_aadhar = st.text_input("Search by Aadhar")

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# Get already found Aadhar numbers
c.execute("SELECT aadhar FROM already_found")
found_aadhar = [row[0] for row in c.fetchall()]

query = """
SELECT id, name, age, aadhar,
       last_seen, contact, image
FROM missing_persons
"""

conditions = []
values = []

# Exclude already found
if found_aadhar:
    placeholders = ",".join(["?"] * len(found_aadhar))
    conditions.append(f"aadhar NOT IN ({placeholders})")
    values.extend(found_aadhar)

# Search filters
if search_name:
    conditions.append("name LIKE ?")
    values.append(f"%{search_name}%")

if search_aadhar:
    conditions.append("aadhar LIKE ?")
    values.append(f"%{search_aadhar}%")

if conditions:
    query += " WHERE " + " AND ".join(conditions)

c.execute(query, values)
rows = c.fetchall()
conn.close()


if not rows:
    st.success("No pending cases 🎉")

else:
    for row in rows:

        record_id = row[0]
        name = row[1]

        st.markdown("---")
        st.subheader(name)

        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(Image.open(io.BytesIO(row[6])), width=220)

        with col2:
            st.write("Age:", row[2])
            st.write("Aadhar:", row[3])
            st.write("Last Seen:", row[4])
            st.write("Contact:", row[5])

            if st.button(f"🗑 Delete {name}", key=f"delete_{record_id}"):

                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()

                c.execute(
                    "DELETE FROM missing_persons WHERE id = ?",
                    (record_id,)
                )

                conn.commit()
                conn.close()

                st.success("Record Deleted Successfully")
                st.rerun()