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
st.write("## 📌 Notice")

_, col = st.columns([9, 1])
with col: st.page_link('pages/add_post.py', label='Add Post', icon=':material/add_comment:')

postDB = PostDB()
posts = postDB.get_posts()

if posts:
    st.info(f"총 {len(posts)}개의 게시글이 있습니다.")
    df = pd.DataFrame(posts, columns=['post_id', 'title', 'author', 'content', 'date'])
    df['title'] = df.apply(lambda x: f'[{x["title"]}](view_post?post_id={x["post_id"]})', axis=1)
    df['author'] = df.apply(lambda x: f"`{x['author']}`", axis=1)
    df['tag'] = df.apply(lambda x: f":red-badge[:material/star: Favorite]", axis=1)
    df.drop(columns=['content', 'post_id'], inplace=True)
    df.sort_values(by='date', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.index += 1
    
    df_md = df.to_markdown(index=True)
    st.write(df_md)
    
else:
    st.info("등록된 게시글이 없습니다.")

