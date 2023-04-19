from base_memory import MemoryObject
from plan import update_plan, Plan, regenerate_plan
from reflection import reflect
from retrieval import retrieval_function
from utility import text_generate


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

    def remove_existing_plans(self):
        #TODO remove only future plans
        self.memory = [memory_object for memory_object in self.memory if not isinstance(memory_object, Plan)]

    def get(self, n):
        return self.memory[:n]

    def get_decomposable_plans(self):
        return [memory_object for memory_object in self.memory if isinstance(memory_object, Plan) and memory_object.duration > 15*60]

    def decompose_plans(self):
        while True:
            # TODO paper does just-in-time decomposition
            plans = self.get_decomposable_plans()
            if not plans:
                break
            for plan in plans:
                self.memory.remove(plan)
                self.add_all(plan.decompose())


class Agent:
    def __init__(self, first_name, last_name, age, description):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.memory_stream = MemoryStream()

        # Put initial description in agent
        for desc in description.split("; "):
            self.memory_stream.add(MemoryObject(desc))

        # Initialize summary description
        self.summary_description = ""
        self.update_summary_description()

        # Initialize plan
        self.plan = regenerate_plan(self)
        self.memory_stream.decompose_plans()

    def on_observation(self, observation):
        # Save observation in memory
        memory_object = MemoryObject(observation)
        self.memory_stream.add(memory_object)

        # Check for reflections
        reflections = reflect(self, self.memory_stream)
        if reflections:
            self.memory_stream.add_all(reflections)

        # Check for plan changes
        new_plans = update_plan(self, observation, self.memory_stream)
        if new_plans:
            self.memory_stream.remove_existing_plans()
            self.memory_stream.add_all(new_plans)
            self.memory_stream.decompose_plans()

        #TODO Update summary description at "regular" intervals
        self.update_summary_description()

    def update_summary_description(self):
        def _helper(query, question):
            relevant_memories = retrieval_function(self.memory_stream, query, n=5)
            prompt = question + "\n" + "\n-".join([memory.nlp_description for memory in relevant_memories])
            response = text_generate(prompt)
            return response

        core_characteristics = _helper(self.get_full_name() + "'s core characteristics.", "How would one describe " + self.first_name + "'s core characteristics given the following statements?")
        recent_progress = _helper(self.get_full_name() + "'s feeling about his/her recent progress in life.", "How would one describe " + self.first_name + "'s feeling about his/her recent progress in life given the following statements?")
        daily_occupation = _helper(self.get_full_name() + "'s current daily occupation.", "How would one describe " + self.first_name + "'s current daily occupation given the following statements?")

        self.summary_description = "Name: " + self.get_full_name() + "(age: " + self.age + ")\n" \
                                   + core_characteristics + "\n" + recent_progress + "\n" + daily_occupation

    def get_full_name(self):
        return self.first_name + " " + self.last_name


