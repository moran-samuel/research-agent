from urllib import response
import json

import streamlit as st
import requests

st.title("AI Research Assistant")

question = st.text_input("Ask a research question")

if st.button("Research"):

    with requests.post(
        "http://backend:8000/research", 
        json={"question": question},
        stream=True,
    ) as response:
        lines = response.iter_lines()
 
        # First line contains sources or an error
        first_line = next(lines, None)
        if not first_line:
            st.error("No response from backend.")
        else:
            first = json.loads(first_line)
            if "error" in first:
                st.error(f"Backend error: {first['error']}")
            else:
                sources = first.get("sources", [])
 
                st.subheader("Answer")
 
                # Stream remaining tokens into the UI
                def token_generator():
                    for line in lines:
                        if line:
                            yield line.decode("utf-8") if isinstance(line, bytes) else line
 
                st.write_stream(token_generator())
 
                st.subheader("Sources")
                for s in sources:
                    st.write(f"[{s['title']}]({s['link']})")
