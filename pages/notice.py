import os, sys, json
import streamlit as st
import pandas as pd

from utils.ui import *
from utils.func import *
from utils.post_db import PostDB

# --- Streamlit Page Setting
set_page_config()
set_sidebar()

# --- UI
st.write("### Notice")

st.page_link('pages/add_post.py', label='Add Post', icon=':material/add_comment:')

postDB = PostDB()
posts = postDB.get_posts()

if posts:
    # df = pd.DataFrame(posts, columns=['post_id', 'title', 'author', 'content', 'date'])
    # df['title'] = df.apply(lambda x: f'[{x["title"]}](view_post?post_id={x["post_id"]})', axis=1)
    # df['author'] = df.apply(lambda x: f"`{x['author']}`", axis=1)
    # df.drop(columns=['content', 'post_id'], inplace=True)
    # df.sort_values(by='date', ascending=False, inplace=True)
    # st.table(df)
    

    for post in posts:
        post_id, title, author, _, date = post
        # st.markdown(f'[{title}](view_post?post_id={post_id})', unsafe_allow_html=False)  
        # st.markdown(f'<a href="view_post?post_id={post_id}" target="_self">{title}</a>', unsafe_allow_html=True)
        st.page_link(f'view_post.py', label=title )
else:
    st.info("등록된 게시글이 없습니다.")
