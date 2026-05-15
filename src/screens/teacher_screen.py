import streamlit as st
from src.UI.base_layout import style_base_layout,style_background_dashboard
from src.components.header import header_dashboard 
from src.database.db import create_teacher,check_teacher_exist,teacher_login
def teacher_screen():
    style_base_layout()
    style_background_dashboard()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type=="Register":
        teacher_screen_register()

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    st.h2("Welcome, {teacher_data['teacher_name']}")

def login_teacher(username,password):
    if not username or not password:
        return False
    teacher = teacher_login(username,password)

    if teacher:
        st.session_state.user_role="teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False
def teacher_screen_login():
    c1,c2 = st.columns(2,vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("BACK",type="secondary",key="loginbackbtn",shortcut="control+backspace",icon=":material/arrow_left:"):
            st.session_state["login_type"] = None
            st.rerun()
    st.space()
    st.header("login using password",text_alignment="center")
    teacher_username = st.text_input("Enter Username",placeholder="nitin")
    teacher_password = st.text_input("Enter Password",type="password",placeholder="Enter Password")
    st.divider()
    btnc1 , btnc2 = st.columns(2,gap="large")
    with btnc1:
        if st.button("Login",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            if login_teacher(teacher_username,teacher_password):
                st.toast("WELCOME BACK",icon="😍")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password combo")
    with btnc2:
        if st.button("Register Instead",icon=":material/passkey:",width="stretch",type="primary"):
            st.session_state.teacher_login_type = "Register"


def register_teacher(teacher_username,teacher_name,teacher_password,check_password):
    if not teacher_username or not teacher_name or not teacher_password:
        return False, "All fields are required!"
    if check_teacher_exist(teacher_username):
        return False,"username already taken"
    if teacher_password != check_password:
        return False, "password doesn't match"
    try:
        create_teacher(teacher_username,teacher_name,teacher_password,check_password)
        return True , "Sucessfully Created! Login Now"
    except Exception as e:
        return False,"Unexpected Error!"
    

def teacher_screen_register():
    c1,c2 = st.columns(2,vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("BACK ",type="secondary",key="registerbackbtn",shortcut="control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()
    st.space()
    st.header("Registre your teacher profile",text_alignment="center")
    st.space()
    teacher_username = st.text_input("Enter Username",placeholder="Rohit_785")
    teacher_name = st.text_input("Enter your name",placeholder="Rohit Jat")
    teacher_password = st.text_input("Enter Password",type="password",placeholder="Enter Password")
    check_password = st.text_input("confirm your passwors",type="password",placeholder="confirm your password")
    st.divider()
    btnc1 , btnc2 = st.columns(2,gap="large")
    with btnc1:
        if st.button("Register now",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            success , messege = register_teacher(teacher_username,teacher_name,teacher_password,check_password)
            if success:
                st.success(messege)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(messege)
    with btnc2:
        if st.button("Login Instead",icon=":material/passkey:",width="stretch",type="primary"):
            st.session_state.teacher_login_type = "login"


