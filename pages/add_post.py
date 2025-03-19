import os, sys, json

from datetime import datetime
from time import sleep

import streamlit as st

from utils.post_db import PostDB


postDB = PostDB()

st.write("### Add Post")

title = st.text_input("Title")
author = st.text_input("Author")
content = st.text_area("Content", height=200)
date = st.date_input("Date")
password = st.text_input("Password", type="password")

if st.button("Submit"):
    date = date.strftime("%Y-%m-%d")
    postDB.add_post(title, author, content, date, password)
    st.success("Post Added!")
    sleep(1)
    st.switch_page("pages/notice.py")