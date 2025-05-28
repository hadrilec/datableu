# utils/llm_utils.py

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_prompt(prompt: str):
    """Parse user natural language prompt into structured query fields."""
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a data assistant. Given a user prompt, extract key fields "
                        "as a JSON dictionary: 'indicator' (e.g., CPI, unemployment), "
                        "'region' (e.g., Paris), and 'start_year' (e.g., 2010). "
                        "Respond ONLY with a JSON object."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        message = response.choices[0].message.content.strip()
        return json.loads(message)  # Ensure safe parsing

    except Exception as e:
        return {"error": str(e)}
