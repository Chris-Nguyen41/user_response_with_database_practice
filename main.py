# app.py
import streamlit as st
from database import Session, User_Response

if 'TOKEN' not in st.session_state:
    st.session_state['TOKEN'] = True

st.title("Enter 3 Letters")

if st.session_state['TOKEN']:
    UserMessage = st.text_input("Enter your 3 letters", max_chars=3)
    if len(UserMessage) == 3:
        if UserMessage.isalpha():
            st.success("Response verified")
            if st.button("Submit response to database"):
                with Session() as session:
                    with session.begin():
                        new_entry = User_Response(response=UserMessage)
                        session.add(new_entry)
                        st.success("Response recorded")
        else:
            st.error("Invalid response. Please enter 3 letters only")
elif not st.session_state['TOKEN']:
    st.error("You have already responded")

