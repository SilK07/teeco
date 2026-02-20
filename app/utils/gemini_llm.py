from google import genai
from app.config import GEMINI_API_KEY

gemini_client = genai.Client(api_key=GEMINI_API_KEY)


def generate(prompt: str):
    response = gemini_client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
    )

    return response.text
