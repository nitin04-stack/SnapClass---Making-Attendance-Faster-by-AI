import streamlit as st
from src.components.header import header_home
from src.UI.base_layout import style_base_layout,style_background_dashboard,style_background_home

def home_screen():
    header_home()
    style_base_layout()
    style_background_home()
    # style_background_dashboard()

    col1 , col2 = st.columns(2,gap="large")

    with col1:
        st.header("i am Teacher")
        st.image("https://png.pngtree.com/png-vector/20230729/ourmid/pngtree-picture-of-a-teacher-vector-png-image_7009012.png",width=120)
        if st.button("Teacher_Portal",type="primary",icon=":material/arrow_outward:",icon_position="right"):
            st.session_state["login_type"] = "teacher"
            st.rerun
    with col2:
        st.header("i am Student")
        st.image("https://png.pngtree.com/png-clipart/20250418/original/pngtree-cartoon-cute-little-boy-student-giving-isolated-with-transparent-background-png-image_20720809.png",width=120)
        if st.button("Student_Portal",type="primary",icon=":material/arrow_outward:",icon_position="right"):
            st.session_state["login_type"] = "student"
            st.rerun 
        