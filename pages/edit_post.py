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

st.write("### Edit Post")

post_id = st.query_params.get("post_id", None)

if post_id:
    post = postDB.get_post_by_id(post_id)
    if post:
        post_id, title, author, content, date = post
        title = st.text_input("Title", value=title)
        author = st.text_input("Author", value=author)
        date = st.date_input("Date", value=datetime.strptime(date, "%Y-%m-%d"))
        content = st_quill(value=content, html=True)
        password = st.text_input("Password", type="password")
        if st.button("Submit"):
            date = date.strftime("%Y-%m-%d")
            postDB.update_post(post_id, title, author, content, date, password)
            st.toast("⭐️ Post Updated!")
            sleep(1)
            st.switch_page("pages/notice.py")
    else:
        st.error("Post Not Found!")
        sleep(1)
        st.switch_page("pages/notice.py")
else:
    st.error("Post ID Not Found!")
    sleep(1)
    st.switch_page("pages/notice.py")
