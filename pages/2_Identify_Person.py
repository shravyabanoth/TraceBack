import streamlit as st
from database import match_face, save_found_match
from PIL import Image
import io
import pandas as pd   # ← ADD THIS
st.set_page_config(page_title="Identify Person")

st.title("Identify Person")

photo = st.file_uploader(
    "Upload Photo",
    type=["jpg", "jpeg", "png"]
)

st.subheader("Location")

latitude = st.number_input("Latitude")
longitude = st.number_input("Longitude")

if st.button("Check Match"):

    if photo:

        result = match_face(photo)

        if result:

            st.success("Match Found")

            saved = save_found_match(
                result,
                photo,
                latitude,
                longitude
            )

            if saved:
                st.success("Saved to Matched Cases")

            map_data = pd.DataFrame({
                "lat": [latitude],
                "lon": [longitude]
            })

            st.map(map_data)

            col1, col2 = st.columns(2)

            with col1:
                st.image(photo, width=300)

            with col2:
                st.image(
                    Image.open(io.BytesIO(result["Image"])),
                    width=300
                )

            st.write("Name:", result["Name"])
            st.write("Age:", result["Age"])
            st.write("Contact:", result["Contact"])

        else:
            st.error("No match found")