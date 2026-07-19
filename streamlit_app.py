import uuid
import requests
import streamlit as st

# ======================================================
# Configuration
# ======================================================

API_URL = "https://capstoneiitmdec.onrender.com/chat"

st.set_page_config(
    page_title="NetAssist",
    page_icon="📡",
    layout="centered"
)

# ======================================================
# Sidebar
# ======================================================

with st.sidebar:

    st.title("CapstoneProject")

    st.markdown("## 🤖 NetAssist")

    st.markdown(
        """
Router Support & Troubleshooting Assistant
"""
    )

    st.divider()

    st.markdown("### Supported Routers")

    st.markdown("""
- ✅ TP-Link Archer C5
- ✅ Netgear D7000
""")

    st.divider()

    if st.button("🆕 New Conversation"):

        st.session_state.session_id = str(uuid.uuid4())

        st.session_state.messages = [
            {
                "role": "assistant",
                "content":
"""
Hello!

Welcome to **NetAssist**.

I currently support:

• TP-Link Archer C5

• Netgear D7000

Please describe your issue.

If possible, include your router model.
"""
            }
        ]

        st.rerun()

# ======================================================
# Session State
# ======================================================

if "session_id" not in st.session_state:

    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:

    st.session_state.messages = [

        {
            "role": "assistant",

            "content":
"""
Hello!

Welcome to **NetAssist**.

I currently support:

• TP-Link Archer C5

• Netgear D7000

Please describe your issue.

If possible, include your router model.
"""
        }

    ]

# ======================================================
# Header
# ======================================================

st.title("📡 NetAssist")

st.caption(
    "AI-powered Router Support Assistant"
)

# ======================================================
# Display Conversation
# ======================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ======================================================
# User Input
# ======================================================

prompt = st.chat_input(
    "Describe your issue..."
)

if prompt:

    # Display user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    # Query backend

    with st.chat_message("assistant"):

        with st.spinner("NetAssist is thinking..."):

            try:

                response = requests.post(

                    API_URL,

                    json={

                        "session_id":
                            st.session_state.session_id,

                        "message":
                            prompt

                    },

                    timeout=60

                )

                response.raise_for_status()

                data = response.json()

                assistant_reply = data["messages"][-1]

                st.markdown(
                    assistant_reply
                )

                st.session_state.messages.append(

                    {

                        "role": "assistant",

                        "content": assistant_reply

                    }

                )

                # Optional escalation banner

                if data.get("next_action") == "ESCALATE":

                    st.warning(
                        "⚠ This issue requires escalation to Tier 2 support."
                    )

            except Exception as e:

                error = f"""
Unable to contact the backend.

Error:

{e}
"""

                st.error(error)

                st.session_state.messages.append(

                    {

                        "role": "assistant",

                        "content": error

                    }

                )
