from openai import OpenAI
from utils.config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def call_openai_llm(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=Config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()
