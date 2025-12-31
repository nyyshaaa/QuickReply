
from google import genai
from typing import List, Dict

client = genai.Client()


SYSTEM_PROMPT = """

"""

class LLMError(Exception):
    pass


def generate_reply(
    history: List[Dict[str, str]],
    user_message: str,
) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt_parts = [
            SYSTEM_PROMPT,
            "\nConversation history:\n",
        ]

        for msg in history:
            role = "User" if msg["sender"] == "user" else "Agent"
            prompt_parts.append(f"{role}: {msg['text']}\n")

        prompt_parts.append(f"User: {user_message}\nAgent:")

        response = model.generate_content(
            "".join(prompt_parts),
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 300,
            },
        )

        if not response.text:
            raise LLMError("Empty response from LLM")

        return response.text.strip()

    except Exception as e:
        raise LLMError(str(e))
