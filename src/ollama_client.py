import os
import requests


# ============================================================
# LLM CONFIGURATION
# ============================================================

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "ollama"
).lower()

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://127.0.0.1:11434/api/generate"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:3b"
)

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "qwen/qwen3.8-27b"
)


# ============================================================
# OLLAMA
# ============================================================

def _generate_ollama_response(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
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


# ============================================================
# GROQ
# ============================================================

def _generate_groq_response(prompt):
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        choices = data.get("choices", [])

        if not choices:
            raise RuntimeError(
                "Groq returned an empty response."
            )

        result = (
            choices[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )

        if not result:
            raise RuntimeError(
                "Groq returned an empty response."
            )

        return result

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Cannot connect to Groq API."
        )

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Groq request timed out."
        )

    except requests.exceptions.RequestException as error:
        error_message = str(error)

        try:
            error_details = response.json()

            error_message = (
                error_details
                .get("error", {})
                .get("message", error_message)
            )

        except Exception:
            pass

        raise RuntimeError(
            f"Groq request failed: {error_message}"
        )


# ============================================================
# UNIFIED LLM FUNCTION
# ============================================================

def generate_ollama_response(prompt):
    """
    Backward-compatible LLM interface.

    Provider is selected using LLM_PROVIDER:

        ollama -> local Ollama + Qwen 2.5 3B
        groq   -> Groq + hosted Qwen model
    """

    if LLM_PROVIDER == "ollama":
        return _generate_ollama_response(prompt)

    if LLM_PROVIDER == "groq":
        return _generate_groq_response(prompt)

    raise RuntimeError(
        f"Unsupported LLM_PROVIDER: '{LLM_PROVIDER}'. "
        "Use 'ollama' or 'groq'."
    )