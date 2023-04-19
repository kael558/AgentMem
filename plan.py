import re
from datetime import datetime

from base_memory import MemoryObject
from retrieval import retrieval_function
from utility import get_prompt_template, text_generate


class Plan(MemoryObject):
    def __init__(self, nlp_description, start_time, duration, location):
        super().__init__(nlp_description)
        self.start_time = start_time
        self.duration = duration
        self.location = location

    def decompose(self):
        if self.duration < 15*60:  # 15 minutes
            return [self]
        prompt = get_prompt_template("prompts/decompose_plan.prompt", plan=self.nlp_description)
        decomposed_plans = text_generate(prompt)
        decomposed_plans = parse_plans_from_llm(decomposed_plans)
        return decomposed_plans


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
    return response


def parse_plans_from_llm(plans):
    plans = re.split(r',?\d+\)\s*', plans)[1:]

    plans = [plan.strip() for plan in plans]

    # TODO extract start time, duration, location
    plans = [Plan(plan, datetime.now(), 1, "home") for plan in plans]
    return plans


def regenerate_plan(agent):
    prompt = get_prompt_template("prompts/regenerate_plan.prompt",
                                 agent_summary_description=agent.summary_description,
                                 date=datetime.now().strftime("%m %d %H:%M %I"),
                                 agent_first_name=agent.first_name
                                 )

    plans = text_generate(prompt)

    return parse_plans_from_llm(plans)


def update_plan(agent, observation, situation_context):
    if not check_update_plan(agent, observation, situation_context):
        return None

    plan = regenerate_plan(agent)
    return plan
