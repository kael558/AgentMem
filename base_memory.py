from datetime import datetime

from utility import get_prompt_template, text_generate


def get_importance(nlp_description):
    prompt_template = get_prompt_template("prompts/importance.prompt", description=nlp_description)
    return float(text_generate(prompt_template))


class MemoryObject:
    def __init__(self, nlp_description):
        self.nlp_description = nlp_description
        self.creation_timestamp = datetime.now()
        self.last_access_timestamp = datetime.now()
        self.importance = get_importance(nlp_description)


