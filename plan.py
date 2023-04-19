import re
from datetime import datetime

from memory_stream import MemoryObject
from retrieval import retrieval_function
from utility import get_prompt_template, text_generate


class Plan(MemoryObject):
    def __init__(self, nlp_description, start_time, duration, location):
        super().__init__(nlp_description)
        self.start_time = start_time
        self.duration = duration
        self.location = location

    def decompose(self):
        # Fine grain actions with smaller durations
        pass


def get_situation_context(observer, observed_entity):
    query1 = f"What is {observer}'s relationship with {observed_entity}?"
    query2 = f"{observed_entity} is {observed_entity.action}?"
    relevant_memories = retrieval_function(query1, n=5) + retrieval_function(query2, n=5)
    return relevant_memories


def check_update_plan(agent, observation, situation_context):
    prompt = get_prompt_template("prompts/check_update_plan.prompt",
                                 agent_summary_description=agent.summary_description,
                                 date=datetime.now().strftime("%m %d %H:%M %I"),
                                 agent_name=agent.get_full_name(),
                                 agent_status=agent.status,
                                 observation=observation,
                                 agent_context=situation_context,
                                 agent_first_name=agent.name.split(" ")[0],
                                 )
    response = text_generate(prompt)

    # TODO check if response is yes or no
    return response.choices[0].text


def regenerate_plan(agent):
    prompt = get_prompt_template("prompts/initial_plan.prompt",
                                 agent_summary_description=agent.summary_description,
                                 date=datetime.now().strftime("%m %d %H:%M %I"),
                                 agent_first_name=agent.first_name
                                 )

    plans = text_generate(prompt)
    plans = re.split(r',?\d+\)\s*', plans)[1:]

    plans = [plan.strip() for plan in plans]

    # TODO extract start time, duration, location
    plans = [Plan(plan, datetime.now(), 1, "home") for plan in plans]
    return plans


def decompose_plan(memory_stream):
    plans = memory_stream.get_plans()

    for plan in plans:
        plan.decompose()



def update_plan(agent, observation, situation_context):
    if not check_update_plan(agent, observation, situation_context):
        return None




    pass