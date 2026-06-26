import streamlit as st
from src.database.db import create_subject
import segno
import io

@st.dialog("Share class link")
def share_subject_dialog(subject_name,subject_code):
   app_domain = "snapclass-main.streamlit.app"
   join_url = f"{app_domain}?join_code={subject_code}"
   st.header("scan the QR code to join the class")
   qr = segno.make(join_url)
   out = io.BytesIO()
   qr.save(out,kind = "png",scale=10,border=1)

   col1,col2 = st.columns(2)
   with col1:
      st.markdown("###copy link")
      st.code(join_url,language="text")
      st.code(subject_code, language="text")
      st.info("Share this code with your students to let them join the class")
   with col2:
     st.markdown("### copy link")
     st.image(out.getvalue(),caption = "QRCode for joining the class")
      