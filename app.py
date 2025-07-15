import streamlit as st
from ui import main

# ✅ Μπαινει εδώ στην αρχή!
st.set_page_config(page_title="Law Checker", layout="centered", page_icon="⚖️")

def main_app():
    main.render()

if __name__ == "__main__":
    main_app()
