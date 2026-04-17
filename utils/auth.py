import bcrypt
import streamlit as st


def require_password() -> bool:
    if st.session_state.get("authenticated"):
        return True

    st.title("House Maintenance Tracker")

    _, col, _ = st.columns([2, 1, 2])
    with col:
        with st.form("login_form"):
            pw = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Sign in", type="primary", use_container_width=True)

    if not submitted:
        st.stop()

    if not pw:
        st.error("Please enter a password.")
        st.stop()

    stored_raw = st.secrets.get("password_hash", "").strip()
    if not stored_raw:
        st.error("No password hash configured in secrets.")
        st.stop()

    if bcrypt.checkpw(pw.encode(), stored_raw.encode()):
        st.session_state["authenticated"] = True
        st.rerun()
    else:
        st.error("Incorrect password.")
        st.stop()

    return False


def logout_button() -> None:
    if st.sidebar.button("Log out", use_container_width=True):
        st.session_state.clear()
        st.rerun()
