# app.py
import streamlit as st
from database import SessionLocal, User_Response
from sqlalchemy.exc import IntegrityError

st.title("Enter 3 Letters")

user_response = st.text_input("Enter your 3 letters", max_chars=3)

if user_response.isalpha() and len(user_response) == 3:
    st.success("Response verified")

    if st.button("Submit response to be saved"):
        with SessionLocal() as session:
            try:
                new_entry = User_Response(response=user_response)
                session.add(new_entry)
                session.commit()
                st.success("Response recorded")
            except:
                session.rollback()
                st.error("An error has occurred while saving your response. Please try again later")
else:
    st.error("Invalid response. Please enter 3 letters only")

