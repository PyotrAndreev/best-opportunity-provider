from openai import OpenAI
from .config import OPEN_AI_API_KEY

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = OPEN_AI_API_KEY
)


def _make_completion(message: str):
    """
    Generates a chat completion response from the OpenAI API using the provided message.

    Args:
        message (str): The input message to send to the AI model.

    Returns:
        OpenAI Response: The completion response from the API, which includes chat options in streaming format.
    """

    return client.chat.completions.create(
        model="meta/llama-3.3-70b-instruct",
        messages=[{"role": "user", "content": message}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )


def query(message: str) -> str:
    """
    Sends a message to the OpenAI API and returns the concatenated response from the AI model.

    Args:
        message (str): The input message to send to the AI model.

    Returns:
        str: The response content returned by the AI model after processing the input message.
    """

    completion = _make_completion(message)
    chunks_content = []
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            chunks_content.append(chunk.choices[0].delta.content)
    return ''.join(chunks_content)
