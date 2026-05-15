import streamlit as st
from src.UI.base_layout import style_base_layout,style_background_dashboard
from src.components.header import header_dashboard 
from PIL import Image
import numpy as np
def student_screen():
    style_base_layout()
    style_background_dashboard()

    if "student_login_type" not in st.session_state or st.session_state.student_login_type=="login":
        student_screen_login()
    elif st.session_state.student_login_type=="Register":
        student_screen_register()

def student_screen_login():
    c1,c2 = st.columns(2,vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("BACK",type="secondary",key="loginbackbtn",shortcut="control+backspace",icon=":material/arrow_left:"):
            st.session_state["login_type"] = None
            st.rerun()
    st.space()
    st.header("login with FaceId",text_alignment="center")
    st.space()
    photo_source=st.camera_input("position your face in center")

    if photo_source:
        np.array(Image.open(photo_source))
        