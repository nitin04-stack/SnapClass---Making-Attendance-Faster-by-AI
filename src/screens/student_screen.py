import streamlit as st
from src.UI.base_layout import style_base_layout,style_background_dashboard
from src.components.header import header_dashboard 
from src.database.db import create_teacher,check_teacher_exist,teacher_login
from PIL import Image
import numpy as np
from src.pipelines.face_pipelines import predict_attendance,get_face_embeddings,train_classifier
from src.database.db import get_all_students,create_student,get_student_subjects,get_student_attendance,unenroll_student_from_subject
from src.pipelines.voice_pipelines import get_voice_embedding
import time
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data["student_id"]
    c1,c2 = st.columns(2,vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {student_data['name']}""")
        if st.button("Logout",type="secondary",key="loginbackbtn",shortcut="control+backspace",icon=":material/arrow_left:"):
            st.session_state["is_logged_in"] = False
            del st.session_state.student_data
            st.rerun()
    st.space()
    c1,c2 = st.columns(2)
    with c1:
        st.header("Your Enrolled Subjects")
    with c2:
        if st.button("Enroll subjects",type="primary",icon=":material/add:"):
            enroll_dialog()
    st.divider()
    with st.spinner("Loading your subjects..."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)
    stats_map = {}
    for log in logs:
        sid = log["subject_id"]

        if sid not in stats_map:
            stats_map[sid] = {"total": 0,"attended": 0}
        stats_map[sid]["total"] += 1

        if log.get("is_persent"):
            stats_map[sid]["attended"] += 1
    cols = st.columns(2)

    for i,sub_node in enumerate(subjects):
        sub = sub_node["subjects"]
        sid = sub["subject_id"]
        stats = stats_map.get(sid,{"total": 0,"attended": 0})

        def unenroll_button():
            if st.button("Unenroll from this course",type="tertiary",width = "stretch",key=f"unenroll_{sid}",icon = ":material/delete_forever:"):
                unenroll_student_from_subject(student_id,sid)
                st.toast(f"Unenrolled from {sub['name']} Successfully")
                st.rerun()
        with cols[i % 2]:
            subject_card(
            name=sub["name"],
            code = sub["subject_code"],
            section = sub["section"],
            stats = [
                ("📅","Total",stats["total"]),
                ("✅","Attended",stats["attended"]),
            ],
            footer_callback = unenroll_button
        )


def student_screen():
    show_registration = False
    style_base_layout()
    style_background_dashboard()

    if "student_data" in st.session_state:
        student_dashboard()
        return
    c1,c2 = st.columns(2,vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("BACK",type="secondary",key="loginbackbtn",shortcut="control+backspace",icon=":material/arrow_left:"):
            st.session_state["login_type"] = None
            st.rerun()

    st.space()
    st.header("login using Face id",text_alignment="center")
    st.space()

    photo_source = st.camera_input("Position your face in center")
    if photo_source:
        img = np.array(Image.open(photo_source))
        with st.spinner("AI is scanning"):
            detected,all_ids,num_faces = predict_attendance(img)
            if num_faces ==0:
                st.warning("Face not found, try again")
            elif num_faces > 1:
                st.warning("Multiple faces detected, try again")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s["student_id"] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}")
                        import time
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not recognized!, You might be a new student!")
                    show_registration = True
    if show_registration:
        with st.container(border = True):
            st.header("Register new Profile")
            new_name = st.text_input("Enter your name",placeholder="E.g. Yogesh")

            st.subheader("optional:Voice Enrollment")
            st.info("Enroll youself for voice attendance")

            audio_data = None

            try:
                audio_data = st.audio_input("Record a short clip of your voice (3-5 seconds) Like I am Present, My name is Rohit")
            except Exception:
                st.error("audio input error, try again")
            if st.button("create profile",type="primary"):
                if new_name:
                    with st.spinner("Creating Profile"):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())
                            response_data = create_student(name = new_name,face_embedding = face_emb, voice_embedding = voice_emb)
                            if response_data:
                                train_classifier()

                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Welcome {new_name}, Profile Created!")
                                import time
                                time.sleep(1)
                                st.rerun()
                                st.success("Profile Created! Please login again")
                        else:
                            st.error("Face not detected, try again with clear face visibility for Registration")        
                else:
                    st.warning("Name is required to create profile")

