import streamlit as st
import requests

st.set_page_config(page_title="Deep Research Agent", layout="wide")

st.title("🧠 Technical Research Agent")

user_id = st.text_input("User ID", value="u1")

mode = st.radio(
    "Select Mode",
    ["quick", "deep"],
    horizontal=True
)

query = st.text_area("Enter your technical query")

if st.button("Run Agent"):

    with st.spinner("Thinking..."):

        try:
            response = requests.post(
                "http://127.0.0.1:8000/query",
                json={
                    "user_id": user_id,
                    "query": query,
                    "mode": mode
                },
                timeout=120
            )

            if response.status_code != 200:
                st.error(f"FastAPI Error: {response.text}")
                st.stop()

            data = response.json()

            st.subheader("Answer")
            st.write(data.get("answer"))

            st.subheader("Memory Used")
            st.write(data.get("memory_used"))

            st.subheader("Docs Used (Deep Mode)")
            for doc in data.get("docs_used", []):
                with st.expander("Retrieved Chunk"):
                    st.write(doc)

        except Exception as e:
            st.error(f"Request Failed: {e}")