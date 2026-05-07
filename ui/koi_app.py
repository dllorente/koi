import streamlit as st

from ui.api_client import (
    get_me,
    login,
    send_chat_message,
    list_chat_sessions,
    get_chat_messages,
)

st.set_page_config(page_title="Koi", page_icon="🐟", layout="wide")


def toggle_debug() -> None:
    st.session_state.show_debug = not st.session_state.show_debug


def init_session_state() -> None:

    if "access_token" not in st.session_state:
        st.session_state.access_token = None

    if "current_user" not in st.session_state:
        st.session_state.current_user = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "session_id" not in st.session_state:
        new_session()

    if "available_sessions" not in st.session_state:
        st.session_state.available_sessions = []

    if "selected_session_id" not in st.session_state:
        st.session_state.selected_session_id = None

    if "show_debug" not in st.session_state:
        st.session_state.show_debug = False

    if "sessions_loaded" not in st.session_state:
        st.session_state.sessions_loaded = False


def clear_chat() -> None:
    st.session_state.messages = []


def new_session() -> None:
    st.session_state.messages = []
    st.session_state.session_id = "default"
    st.session_state.selected_session_id = None


def logout() -> None:
    st.session_state.access_token = None
    st.session_state.current_user = None
    st.session_state.messages = []
    st.session_state.session_id = "default"
    st.session_state.available_sessions = []
    st.session_state.selected_session_id = None
    st.session_state.sessions_loaded = False


def refresh_sessions() -> None:
    if not st.session_state.access_token:
        st.session_state.available_sessions = []
        st.session_state.sessions_loaded = False
        return

    try:
        st.session_state.available_sessions = list_chat_sessions(
            st.session_state.access_token
        )

        session_ids = [s["session_id"] for s in st.session_state.available_sessions]

        if st.session_state.selected_session_id not in session_ids:
            st.session_state.selected_session_id = (
                st.session_state.session_id
                if st.session_state.session_id in session_ids
                else (session_ids[0] if session_ids else None)
            )

        st.session_state.sessions_loaded = True
    except Exception:
        st.session_state.available_sessions = []
        st.session_state.sessions_loaded = False


def load_session_messages(session_id: str) -> None:
    if not st.session_state.access_token or not session_id:
        return

    try:
        response = get_chat_messages(
            access_token=st.session_state.access_token,
            session_id=session_id,
        )
        messages = response.get("messages", [])

        st.session_state.messages = [
            {
                "role": message["role"],
                "content": message["content"],
                "meta": (
                    {
                        "intent": message.get("intent"),
                        "tools_used": (
                            [message["tool_name"]] if message.get("tool_name") else []
                        ),
                        "needs_clarification": message.get(
                            "needs_clarification", False
                        ),
                        "clarification_question": message.get("clarification_question"),
                        "decision_confidence": message.get("decision_confidence"),
                        "decision_reason": message.get("decision_reason"),
                    }
                    if message["role"] == "assistant"
                    else None
                ),
            }
            for message in messages
        ]

        st.session_state.session_id = session_id
        st.session_state.selected_session_id = session_id

    except Exception as exc:
        st.error(f"Failed to load session messages: {exc}")


def submit_user_message(prompt: str) -> None:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
            "meta": None,
        }
    )

    try:
        response = send_chat_message(
            access_token=st.session_state.access_token,
            message=prompt,
            session_id=st.session_state.session_id,
        )

        if response.get("session_id"):
            st.session_state.session_id = response["session_id"]
            st.session_state.selected_session_id = response["session_id"]
            refresh_sessions()

        answer = response.get("answer", "No answer returned.")

        assistant_meta = {
            "intent": response.get("intent"),
            "tools_used": response.get("tools_used", []),
            "needs_clarification": response.get("needs_clarification", False),
            "clarification_question": response.get("clarification_question"),
            "decision_confidence": response.get("decision_confidence"),
            "decision_reason": response.get("decision_reason"),
        }

    except Exception as exc:
        answer = f"Error: {exc}"
        assistant_meta = None

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "meta": assistant_meta,
        }
    )


def render_message_meta(meta: dict | None) -> None:
    if not meta:
        return

    intent = meta.get("intent")
    tools_used = meta.get("tools_used", [])
    confidence = meta.get("decision_confidence")
    needs_clarification = meta.get("needs_clarification", False)
    clarification_question = meta.get("clarification_question")
    reason = meta.get("decision_reason")

    chips = []

    if intent:
        chips.append(f"🧭 `{intent}`")

    for tool in tools_used:
        chips.append(f"🛠️ `{tool}`")

    if confidence is not None:
        chips.append(f"📊 `{confidence:.2f}`")

    if chips:
        st.caption(" · ".join(chips))

    if reason:
        st.caption(f"📝 {reason}")

    if needs_clarification or clarification_question:
        clarification_parts = []

        if needs_clarification:
            clarification_parts.append("❓ Clarification needed")

        if clarification_question:
            clarification_parts.append(clarification_question)

        st.caption(" · ".join(clarification_parts))


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

        col3, col4 = st.columns(2)

        with col3:
            st.button(
                "Logout",
                key="logout_btn",
                on_click=logout,
                use_container_width=True,
            )

        with col4:
            debug_label = "Hide debug" if st.session_state.show_debug else "Debug"
            st.button(
                debug_label,
                key="toggle_debug_btn",
                on_click=toggle_debug,
                use_container_width=True,
            )

        st.divider()
        st.subheader("My sessions")

        if st.button("Refresh sessions", use_container_width=True):
            refresh_sessions()

        if (
            st.session_state.access_token is not None
            and not st.session_state.sessions_loaded
        ):
            refresh_sessions()

        session_options = {
            s["session_id"]: (
                s.get("title")
                or f"{s['session_id'][:8]}... · {str(s.get('updated_at', ''))[:19]}"
            )
            for s in st.session_state.available_sessions
        }

        if session_options:
            session_ids = list(session_options.keys())

            current_selected = (
                st.session_state.selected_session_id
                if st.session_state.selected_session_id in session_ids
                else session_ids[0]
            )

            selected = st.selectbox(
                "Select a session",
                options=session_ids,
                format_func=lambda x: session_options[x],
                index=session_ids.index(current_selected),
                key="session_selector",
            )
            if st.button("Load selected session", use_container_width=True):
                load_session_messages(selected)
                st.rerun()
        else:
            st.caption("No saved sessions yet.")

        # Info visible y clara
        st.caption(f"Session ID: {st.session_state.session_id}")
        st.caption(f"Messages: {len(st.session_state.messages)}")

    else:
        st.info("Login required")

        email = st.text_input(
            "Email",
            # value="demo@example.com",
            value="iconde@example.com",
            key="login_email",
        )

        password = st.text_input(
            "Password",
            # value="demo123",
            value="koi1457",
            type="password",
            key="login_password",
        )

        if st.button("Login", key="login_btn", use_container_width=True):
            try:
                auth_data = login(email, password)
                st.session_state.access_token = auth_data["access_token"]
                st.session_state.current_user = get_me(st.session_state.access_token)
                refresh_sessions()
                st.rerun()
            except Exception as exc:
                st.error(f"Login failed: {exc}")

if st.session_state.show_debug:
    st.markdown("### Debug session")
    st.json(
        {
            "access_token": st.session_state.access_token,
            "current_user": st.session_state.current_user,
            "session_id": st.session_state.session_id,
            "selected_session_id": st.session_state.selected_session_id,
            "messages_count": len(st.session_state.messages),
            "available_sessions_count": len(st.session_state.available_sessions),
        }
    )
    st.divider()

if st.session_state.access_token is None:
    st.warning("Please log in to start chatting.")
    st.stop()


if st.session_state.current_user is not None:
    st.subheader(f"Welcome, {st.session_state.current_user.get('full_name', 'user')}")

# Render del historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            render_message_meta(message.get("meta"))

if prompt := st.chat_input("Ask Koi something about your banking products..."):
    submit_user_message(prompt)
    st.rerun()
