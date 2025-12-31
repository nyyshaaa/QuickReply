
import google.genai as genai
from backend.config.settings import config_settings

_gem_client = genai.Client(
    api_key=config_settings.GEMINI_API_KEY
)

_gem_model = "gemini-2.5-flash"