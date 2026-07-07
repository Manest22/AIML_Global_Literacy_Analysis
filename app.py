import streamlit as st

st.set_page_config(
    page_title="Global Literacy Analysis",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Global Literacy Analysis Dashboard")

st.markdown("""
Welcome to the Global Literacy Analysis Dashboard.

Use the sidebar to navigate between:

- 📊 SQL Query Executor
- 📈 EDA Visualizations
- 🌍 Country Profile

This project analyzes global literacy, GDP, and education indicators using Python, SQLite, and Streamlit.
""")

st.success("Project loaded successfully!")