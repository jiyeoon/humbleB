import os, sys

import streamlit as st

def set_sidebar():
    st.sidebar.page_link('home.py', label='Home', icon=':material/home:')
    st.sidebar.page_link('pages/member.py', label='Member', icon=':material/group:')
    st.sidebar.page_link('pages/schedule.py', label='Schedule', icon=':material/calendar_month:')
    st.sidebar.page_link('https://www.instagram.com/humblebee_tennis/', label='Instagram', icon=':material/favorite:')


