import requests
import json

def ask_llm(system_message, user_message):
    response = requests.post(
        "http://host.docker.internal:11434/v1/chat/completions",
        json={
            "model": "llama3.1",
            "stream": True,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ]
        },
        stream=True,
        timeout=120,
    )

    response.raise_for_status()

    for line in response.iter_lines():
        if not line:
            continue
        # SSE lines are prefixed with "data: "
        raw = line.decode("utf-8").removeprefix("data: ")
        if raw == "[DONE]":
            break
        try:
            token = json.loads(raw)["choices"][0]["delta"].get("content", "")
            if token:
                yield token
        except (json.JSONDecodeError, KeyError):
            continue