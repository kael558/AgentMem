import numpy as np
import openai
from datetime import datetime

def text_generate(prompt: str) -> str:
    # Generate text from prompt
    return openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )

def text_embed(text: str) -> np.array:
    # Embed text
    text = text.replace("\n", " ")
    return openai.Embedding.create(
        model="text-embedding-ada-002",
        input=[text]
    )['data'][0]['embedding']

def get_prompt_template(prompt_file, **kwargs):
    with open(prompt_file) as f:
        prompt = "".join(f.readlines())
        prompt = prompt.format(**kwargs)
        return prompt


