import collections
import os
from datetime import datetime
import openai
import numpy as np
from numpy.linalg import norm

from dotenv import load_dotenv

from memory_stream import MemoryStream


class Agent:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.memory_stream = MemoryStream()
        self.summary_description = ""


    def start(self):
        # initial plan
        # decompose plan
        # receive observation
        # handle reflection
        # handle plan change
        pass

    def handle_observation(self, observation):
        # update summary description
        # update memory stream
        # update plan
        pass


    def update_summary_description(self):
        query = self.name + "'s core characteristics."
        """
        cached summary =
        name, age, and traits
        name's core characteristics
        name's current daily occupation
        name's feeling about his/her recent progress in life
        """


    def summary_description(self):
       pass

if __name__ == "__main__":
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt_template = get_prompt_template("prompts/importance.prompt")
    p = prompt_template.format(description="yolo")
    print(p)
















