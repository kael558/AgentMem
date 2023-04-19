import collections
import os
from datetime import datetime
import openai
import numpy as np
from numpy.linalg import norm

from dotenv import load_dotenv




if __name__ == "__main__":
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt_template = get_prompt_template("prompts/importance.prompt")
    p = prompt_template.format(description="yolo")
    print(p)
















