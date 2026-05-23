import streamlit as st
import sqlite3
from database import create_tables

st.set_page_config(page_title="Dashboard")

create_tables()

st.title("Dashboard")

conn = sqlite3.connect("missing_person.db")
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM missing_persons")
total_missing = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM already_found")
total_found = c.fetchone()[0]

c.execute("""
SELECT COUNT(*)
FROM missing_persons
WHERE aadhar NOT IN (
    SELECT aadhar FROM already_found
)
""")

total_active = c.fetchone()[0]

conn.close()

st.markdown("## Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Missing", total_missing)
col2.metric("Matched", total_found)
col3.metric("Active Cases", total_active)

st.markdown("---")

