
import google.genai as genai
from backend.config.settings import config_settings

client = genai.Client(api_key=config_settings.GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello in one sentence."
)

print(response.text)
