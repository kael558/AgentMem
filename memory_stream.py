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

class Plan(MemoryObject):
    def __init__(self, nlp_description, start_time, duration, location):
        super().__init__(nlp_description)
        self.start_time = start_time
        self.duration = duration
        self.location = location

    def decompose(self):
        # Fine grain actions with smaller durations
        pass


class Reflection(MemoryObject):
    def __init__(self, nlp_description, memory_objects):
        super().__init__(nlp_description)
        self.memory_objects = memory_objects


class MemoryStream:
    memory = []

    def add(self, memory_object):
        self.memory.append(memory_object)

    def get(self, n):
        return self.memory[:n]


