import requests


def ask_llm(prompt):
    response = requests.post(
        "http://host.docker.internal:11434/v1/completions",
        json={
            "model": "llama3.1",
            "prompt": prompt,
        },
        timeout=60,
    )
    print("LLM response:", response.status_code, response.text)
    response.raise_for_status()
    data = response.json()
    text = data.get("choices", [{}])[0].get("text", "")
    if not text.strip():
        raise ValueError(
            f"LLM returned empty completion, finish_reason={data.get('choices',[{}])[0].get('finish_reason')} response={data}"
        )
    return text.strip()
