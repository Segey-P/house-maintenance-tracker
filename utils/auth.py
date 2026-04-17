"""Password gate — same pattern as project-management-hub.

To protect the app, add this at the very top of app.py:

    from utils.auth import require_password, logout_button
    require_password()

And call logout_button() somewhere in the sidebar.
"""
import bcrypt
import streamlit as st


def require_password() -> bool:
    if st.session_state.get("authenticated"):
        return True

    st.title("House Maintenance Tracker")
    st.caption("Enter password to continue.")

    pw = st.text_input("Password", type="password", label_visibility="collapsed")
    if not pw:
        st.stop()

    stored = st.secrets.get("password_hash", "").encode()
    if not stored:
        st.error("No password hash configured in secrets. See README.")
        st.stop()

    if bcrypt.checkpw(pw.encode(), stored):
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
