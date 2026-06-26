import streamlit as st
import requests

st.title("AI Research Assistant")

question = st.text_input("Ask a research question")

if st.button("Research"):

    response = requests.post(
        "http://backend:8000/research", json={"question": question}
    )

    data = response.json()

    if "error" in data:
        st.error(f"Backend error: {data['error']}")

    else:
        st.subheader("Answer")
        st.write(data["answer"])

        st.subheader("Sources")

        for s in data["sources"]:
            st.write(f"[{s['title']}]({s['link']})")
