from datetime import datetime

from retrieval import retrieval_function
from utility import get_prompt_template, text_generate


def get_situation_context(observer, observed_entity):
    query1 = f"What is {observer}'s relationship with {observed_entity}?"
    query2 = f"{observed_entity} is {observed_entity.action}?"
    relevant_memories = retrieval_function(query1, n=5) + retrieval_function(query2, n=5)
    return relevant_memories

def check_update_plan(agent, observation, situation_context):
    prompt = get_prompt_template("prompts/check_update_plan.prompt",
                                 agent_summary_description=agent.summary_description,
                                date=datetime.now().strftime("%m %d %H:%M:%I"),
                                 agent_name=agent.name,
                                 agent_status=agent.status,
                                 observation=observation,
                                 agent_context=situation_context,
                                 agent_first_name=agent.name.split(" ")[0],
                                 )
    response = text_generate(prompt)

    # TODO check if response is yes or no
    return response.choices[0].text
