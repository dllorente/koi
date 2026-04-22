import uuid

import streamlit as st


def init_app_state() -> None:
    if "access_token" not in st.session_state:
        st.session_state.access_token = None

    if "current_user" not in st.session_state:
        st.session_state.current_user = None

    # id de sesión interna real
    if "session_id_internal" not in st.session_state:
        st.session_state.session_id_internal = f"session-{uuid.uuid4()}"

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    if "last_response_data" not in st.session_state:
        st.session_state.last_response_data = None


def reset_chat_state() -> None:
    st.session_state.chat_messages = []
    st.session_state.last_response_data = None


def new_session() -> None:
    st.session_state.session_id_internal = f"session-{uuid.uuid4()}"
    reset_chat_state()
