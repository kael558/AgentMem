from base_memory import MemoryObject
from utility import get_prompt_template, text_generate
import re
from retrieval import retrieval_function


class Reflection(MemoryObject):
    def __init__(self, nlp_description, memory_objects):
        super().__init__(nlp_description)
        self.memory_objects = memory_objects


def check_reflect(memory_stream):
    return memory_stream.importance > 10


def get_high_level_questions(memory_stream):
    memories = memory_stream.get_recent(n=100)
    memories_as_str = "\n".join([memory.nlp_description for memory in memories])

    prompt_template = get_prompt_template("prompts/generate_high_level_questions.prompt",
                                          recent_memory=memories_as_str)
    questions = text_generate(prompt_template)
    questions = questions.split("\n")
    return questions


def extract_insights_with_citations(agent, relevant_memories):
    numbered_memory_list = []
    for i, memory in enumerate(relevant_memories):
        numbered_memory_list.append(f"{i + 1}. {memory.nlp_description}")
    numbered_memory_list = "\n".join(numbered_memory_list)

    prompt_template = get_prompt_template("prompts/extract_insights.prompt",
                                          relevant_memories=numbered_memory_list,
                                          agent_name=agent.get_full_name())
    insights = text_generate(prompt_template)
    insights = insights.split("\n")

    insights_as_tuples = []

    for insight in insights:
        insight, citations = insight.split(" (because of ")
        citations = citations[:-2]  # ).
        citations = citations.split(", ")
        citations = map(int, citations)
        citations = [relevant_memories[i-1] for i in citations]

        # Creating a tuple from the text and the numbers
        output_tuple = (insight, citations)

        insights_as_tuples.append(output_tuple)
    return insights_as_tuples


def reflect(agent, memory_stream):
    if not check_reflect(memory_stream):
        return None

    # Get high level questions
    questions = get_high_level_questions(memory_stream)

    # Get relevant memories
    relevant_memories = []
    for question in questions:
        relevant_memories.append(retrieval_function(memory_stream, question, n=5))

    # Extract insights
    insights = extract_insights_with_citations(agent, relevant_memories)

    # Create reflection
    reflections = [Reflection(insight[0], insight[1]) for insight in insights]

    return reflections
