import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")

client = genai.Client(api_key=api_key)


# ------------------------------------------------------------
# Simple in-memory cache
# ------------------------------------------------------------

_response_cache = {}


def generate_gemini_response(prompt, model="gemini-3.6-flash"):

    cache_key = (model, prompt)

    # Return cached response if available
    if cache_key in _response_cache:
        return _response_cache[cache_key]

    max_retries = 2

    for attempt in range(max_retries + 1):

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            result = response.text

            # Store successful response in cache
            _response_cache[cache_key] = result

            return result

        except Exception as e:

            error_message = str(e)

            # Temporary Gemini server overload
            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < max_retries:
                    time.sleep(2 ** attempt)
                    continue

                raise RuntimeError(
                    "The AI service is temporarily unavailable. "
                    "Please try again in a moment."
                )

            # Rate limit / quota
            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

                raise RuntimeError(
                    "The AI request limit has been reached temporarily. "
                    "Please try again later."
                )

            # Any other Gemini/API error
            raise RuntimeError(
                f"Gemini API error: {error_message}"
            )