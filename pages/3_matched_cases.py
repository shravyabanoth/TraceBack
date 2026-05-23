import streamlit as st
import sqlite3
from PIL import Image
import io
import pandas as pd

st.set_page_config(page_title="Matched Cases")

st.title("Matched Cases")
conn = sqlite3.connect("missing_person.db")
c = conn.cursor()

c.execute("""
SELECT name, age, aadhar,
last_seen, contact,
missing_image, found_image,
found_latitude, found_longitude,
found_date
FROM already_found
ORDER BY id DESC
""")

rows = c.fetchall()
conn.close()

for row in rows:

    st.subheader(row[0])

    col1, col2 = st.columns(2)

    with col1:
        st.image(Image.open(io.BytesIO(row[5])), width=250)

    with col2:
        st.image(Image.open(io.BytesIO(row[6])), width=250)

    st.write("Age:", row[1])
    st.write("Contact:", row[4])
    st.write("Date:", row[9])

    if row[7] and row[8]:

        map_data = pd.DataFrame({
            "lat": [row[7]],
            "lon": [row[8]]
        })

        st.map(map_data)

    st.markdown("---")