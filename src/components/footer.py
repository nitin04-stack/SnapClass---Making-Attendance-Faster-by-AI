import streamlit as st

def footer_Home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; justify-content:center; gap:6px;margin-top:2rem">
            <p style="font-weight: bold; color:white;"> Created by Nitin </p>
        </div>
        """,
        unsafe_allow_html=True
    )