import os
import requests


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://127.0.0.1:11434/api/generate"
)

DEFAULT_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:3b"
)


def generate_ollama_response(prompt, model=DEFAULT_MODEL):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        result = data.get("response", "").strip()

        if not result:
            raise RuntimeError(
                "Ollama returned an empty response."
            )

        return result

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Cannot connect to Ollama. "
            "Make sure 'ollama serve' is running."
        )

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Ollama request timed out."
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Ollama request failed: {error}"
        )