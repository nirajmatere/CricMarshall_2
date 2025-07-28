import openai, httpx, os
from dotenv import load_dotenv

load_dotenv()


client = openai.OpenAI(
    base_url=os.environ["OLLAMA_BASE_URL"],
    api_key="ollama",
    http_client=httpx.Client(
        auth=(os.environ["OLLAMA_USER"], os.environ["OLLAMA_PASS"]),
        base_url=os.environ["OLLAMA_BASE_URL"],
        timeout=600.0,
    )
)
