import os, sys, json
import streamlit as st
import pandas as pd

from utils.ui import *
from utils.func import *
from utils.post_db import PostDB

postDB = PostDB()

query_params = st.query_params
post_id = query_params.get("post_id", None)

if post_id:
    post = postDB.get_post_by_id(post_id)

    if post:
        post_id, title, author, content, date = post
        
        st.write(f"### {title}")
        st.write(f"**Author**: {author}")
        st.write(f"**Date**: {date}")
        st.write(content)
    
    else:
        st.switch_page("pages/notice.py")
else:
    st.switch_page("pages/notice.py")