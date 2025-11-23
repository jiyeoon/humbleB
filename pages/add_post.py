import os, sys, json

from datetime import datetime
from time import sleep

import streamlit as st

from streamlit_quill import st_quill
from utils.func import *
from utils.ui import *
from utils.post_db import PostDB

set_page_config()

postDB = PostDB()

st.write("### Add Post")
# st.markdown("""
# <style>
# .element-container:has(> iframe) {
#   height: 300px;
# }
# </style>
# """, unsafe_allow_html=True)

title = st.text_input("Title")
author = st.text_input("Author")
date = st.date_input("Date")
# content = st.text_area("Content", height=600)
content = st_quill(html=True)
password = st.text_input("Password", type="password")

if st.button("Submit"):
    date = date.strftime("%Y-%m-%d")
    postDB.add_post(title, author, content, date, password)
    st.toast("⭐️ Post Added!")
    sleep(1)
    st.switch_page("pages/notice.py")