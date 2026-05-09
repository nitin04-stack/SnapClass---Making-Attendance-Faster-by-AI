import streamlit as st

def header_home():
    logo_url ="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbYnkynFYE7nvMYGo9oVDCdfgwHe0OMLMQQQ&s"
    st.markdown(
        f"""
        <div style="display:flex; flex_direction:column; align-items:center; justify-content:center; margin-bottom=30px; margin-top:20px;">
            <img src ='{logo_url}' style = "height:50px;" />
            <h1 style = "text-align:center; color:#E0E3FF">SNAP<br/>CLASS</h1>
        </div>
        """,
        unsafe_allow_html=True
    )