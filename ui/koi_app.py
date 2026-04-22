import uuid

import streamlit as st

from ui.api_client import get_me, login, send_chat_message


st.set_page_config(page_title="Koi", page_icon="🐟", layout="wide")


def init_session_state() -> None:
    if "access_token" not in st.session_state:
        st.session_state.access_token = None

    if "current_user" not in st.session_state:
        st.session_state.current_user = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Solo usamos session_id, no conversation_id
    if "session_id" not in st.session_state:
        new_session()


def clear_chat() -> None:
    st.session_state.messages = []


def new_session() -> None:
    # Nueva sesión de chat: vaciamos mensajes y generamos un session_id nuevo
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())


def logout() -> None:
    st.session_state.access_token = None
    st.session_state.current_user = None
    st.session_state.messages = []
    st.session_state.session_id = "default"


init_session_state()

st.title("🐟 Koi Banking Copilot")

with st.sidebar:
    st.header("Session")

    if st.session_state.current_user is not None:
        st.success("Authenticated")
        st.write(
            "Current user:",
            st.session_state.current_user.get("full_name", "Unknown user"),
        )
        st.write(
            "Email:",
            st.session_state.current_user.get("email", "-"),
        )

        col1, col2 = st.columns(2)

        with col1:
            st.button(
                "Clear chat",
                key="clear_chat_btn",
                on_click=clear_chat,
                use_container_width=True,
            )

        with col2:
            st.button(
                "New session",
                key="new_session_btn",
                on_click=new_session,
                use_container_width=True,
            )

        st.button(
            "Logout",
            key="logout_btn",
            on_click=logout,
            use_container_width=True,
        )

        # Info visible y clara
        st.caption(f"Session ID: {st.session_state.session_id}")
        st.caption(f"Messages: {len(st.session_state.messages)}")

        # Debug detallado opcional
        st.divider()
        st.subheader("Debug session")
        st.json(
            {
                "access_token": st.session_state.access_token,
                "current_user": st.session_state.current_user,
                "session_id": st.session_state.session_id,
                "messages_count": len(st.session_state.messages),
            }
        )

    else:
        st.info("Login required")

        email = st.text_input(
            "Email",
            value="demo@example.com",
            key="login_email",
        )

        password = st.text_input(
            "Password",
            value="demo123",
            type="password",
            key="login_password",
        )

        if st.button("Login", key="login_btn", use_container_width=True):
            try:
                auth_data = login(email, password)
                st.session_state.access_token = auth_data["access_token"]
                st.session_state.current_user = get_me(st.session_state.access_token)
                st.rerun()
            except Exception as exc:
                st.error(f"Login failed: {exc}")


if st.session_state.access_token is None:
    st.warning("Please log in to start chatting.")
    st.stop()


if st.session_state.current_user is not None:
    st.subheader(f"Welcome, {st.session_state.current_user.get('full_name', 'user')}")

# Render del historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input de chat
if prompt := st.chat_input("Ask Koi something about your banking products..."):
    # Mensaje de usuario
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Llamada al backend usando session_id real
        response = send_chat_message(
            access_token=st.session_state.access_token,
            message=prompt,
            session_id=st.session_state.session_id,
        )
        if response.get("session_id"):
            st.session_state.session_id = response["session_id"]

        answer = response.get("answer", "No answer returned.")

    except Exception as exc:
        answer = f"Error: {exc}"

    # Mensaje del asistente
    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)
