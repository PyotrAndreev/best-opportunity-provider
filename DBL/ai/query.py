from openai import OpenAI
from .config import OPEN_AI_API_KEY

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = OPEN_AI_API_KEY
)


def _make_completion(message: str):
    return client.chat.completions.create(
        model="meta/llama-3.3-70b-instruct",
        messages=[{"role": "user", "content": message}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )


def query(message: str) -> str:
    completion = _make_completion(message)
    chunks_content = []
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            chunks_content.append(chunk.choices[0].delta.content)
    return ''.join(chunks_content)
