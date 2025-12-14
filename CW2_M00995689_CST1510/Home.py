import streamlit as st
import bcrypt
from app.data.users import insert_user, get_user_by_username

st.set_page_config(page_title="Home", page_icon="🏠", layout="centered")

# Session state setup
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = "analyst"

st.title("🏠 Intelligence Platform")

tab_login, tab_register = st.tabs(["Login", "Register"])

# ---- LOGIN ----
with tab_login:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login", type="primary"):
        user = get_user_by_username(username)
        if user:
            stored_hash = user[2]  # password_hash
            if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                st.session_state.logged_in = True
                st.session_state.username = user[1]
                st.session_state.role = user[3]
                st.success("Login successful")
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("Invalid credentials")
        else:
            st.error("User not found")

# ---- REGISTER ----
with tab_register:
    st.subheader("Register")
    new_user = st.text_input("New username")
    new_pass = st.text_input("New password", type="password")
    role = st.selectbox("Role", ["analyst", "admin", "viewer"])
    if st.button("Register"):
        if new_user and new_pass:
            if get_user_by_username(new_user):
                st.error("Username already exists")
            else:
                insert_user(new_user, new_pass, role=role)
                st.success("Registration successful. Please log in.")
        else:
            st.error("Username and password required")

# Optional quick nav if already logged in
if st.session_state.logged_in:
    st.info(f"Logged in as {st.session_state.username} ({st.session_state.role})")
    if st.button("Go to dashboard"):
        st.switch_page("pages/1_Dashboard.py")