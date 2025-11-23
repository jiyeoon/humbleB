import os, sys, json
import streamlit as st
import pandas as pd

from streamlit_quill import st_quill

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
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Author**: {author}")
        with col2:
            st.write(f"**Date**: {date}")
        
        st.write(f"---")
        st.html(content)
        
        st.link_button("Edit", url=f"edit_post?post_id={post_id}", icon="✏️", type="secondary", use_container_width=True)
    
    else:
        st.switch_page("pages/notice.py")
else:
    st.switch_page("pages/notice.py")