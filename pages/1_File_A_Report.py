import streamlit as st
from database import insert_missing_person

st.set_page_config(page_title="File A Report")

st.title("File A Report")

name = st.text_input("Full Name")

age = st.number_input("Age", min_value=0)

gender = st.selectbox("Gender", ["Male", "Female", "Other"])

aadhar = st.text_input("Aadhar Number")

last_seen = st.text_input("Last Seen Location")

date_missing = st.date_input("Date Missing")

description = st.text_area("Description")

contact = st.text_input("Contact")

photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])


if st.button("Submit Report"):

    if photo:

        success = insert_missing_person(
            name,
            age,
            gender,
            aadhar,
            last_seen,
            date_missing,
            description,
            contact,
            photo
        )

        if success:
            st.success("Report saved")

        else:
            st.error("Face not detected")