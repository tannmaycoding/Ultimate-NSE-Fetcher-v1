import streamlit as st

st.title("Ultimate NSE Fetcher")
st.text("Get The NSE Shares, Broad Market Indices Data and Download Them, See the graph of them")

if st.button("Log In"):
    st.switch_page("pages/page_1.py")

if st.button("Sign Up"):
    st.switch_page("pages/page_2.py")

if st.button("Try as a Guest"):
    st.switch_page("pages/page_4.py")
