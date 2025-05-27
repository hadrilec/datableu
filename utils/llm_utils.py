# utils/llm_utils.py
import openai
from pathlib import Path
import re

with open(str(Path().home()) + '/openai-api-key.txt', 'r') as file:
    secret = file.read()
    
openai.api_key = re.sub(r'\n$', '', secret)

def parse_prompt(prompt):
    system_message = {
        "role": "system",
        "content": (
            "You are a data assistant. Given a user prompt, extract key fields:"
            " indicator (e.g. CPI, unemployment), region (e.g. Paris), start_year (e.g. 2010). "
            "Return only a JSON dictionary."
        )
    }

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            system_message,
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    try:
        text = response["choices"][0]["message"]["content"]
        return eval(text)  # optionally use json.loads()
    except Exception as e:
        return {"error": str(e)}
