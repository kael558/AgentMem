from base_memory import MemoryObject
from plan import update_plan, Plan
from reflection import reflect


class MemoryStream:
    def __init__(self):
        self.memory = []
        self.rolling_sum_importance = 0

    def add(self, memory_object):
        self.memory.append(memory_object)
        self.rolling_sum_importance += memory_object.importance
        if len(self.memory) > 100:
            self.rolling_sum_importance -= self.memory[len(self.memory) - 100].importance

    def add_all(self, memory_objects):
        for memory_object in memory_objects:
            self.add(memory_object)

    def get(self, n):
        return self.memory[:n]

    def get_plans(self):
        return [memory_object for memory_object in self.memory if isinstance(memory_object, Plan)]


class Agent:
    def __init__(self, first_name, last_name, description):
        self.first_name = first_name
        self.last_name = last_name
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

    def on_observation(self, observation):
        # Save observation in memory
        memory_object = MemoryObject(observation)
        self.memory_stream.add(memory_object)

        # Check for reflections
        reflections = reflect(self, self.memory_stream)
        if reflections:
            self.memory_stream.add_all(reflections)

        # Check for plan changes
        plan_changes = update_plan(self, observation, self.memory_stream)
        if plan_changes:
            self.memory_stream.add_all(plan_changes)




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

    def get_full_name(self):
        return self.first_name + " " + self.last_name
