# ============================================================
# COGNITIVE QUEST
# KNOWLEDGE BASE
#
# Knowledge Representation
# Propositional Logic
# Forward Chaining
# Backward Chaining
# ============================================================


class KnowledgeBase:

    def __init__(self):

        # Facts currently known by the AI
        self.facts = set()

        # Logical rules
        self.rules = []


    # ========================================================
    # ADD FACT
    # ========================================================

    def add_fact(self, fact):

        self.facts.add(fact)


    # ========================================================
    # REMOVE FACT
    # ========================================================

    def remove_fact(self, fact):

        if fact in self.facts:

            self.facts.remove(fact)


    # ========================================================
    # CHECK FACT
    # ========================================================

    def has_fact(self, fact):

        return fact in self.facts


    # ========================================================
    # ADD RULE
    # ========================================================

    def add_rule(self, conditions, conclusion):

        rule = {
            "conditions": conditions,
            "conclusion": conclusion
        }

        self.rules.append(rule)


    # ========================================================
    # FORWARD CHAINING
    # ========================================================

    def forward_chain(self):

        new_facts = True

        reasoning_steps = []

        while new_facts:

            new_facts = False

            for rule in self.rules:

                conditions = rule["conditions"]
                conclusion = rule["conclusion"]

                # Check whether all conditions are known
                if all(
                    condition in self.facts
                    for condition in conditions
                ):

                    if conclusion not in self.facts:

                        self.facts.add(
                            conclusion
                        )

                        reasoning_steps.append(
                            f"{conditions} -> {conclusion}"
                        )

                        new_facts = True

        return reasoning_steps


    # ========================================================
    # BACKWARD CHAINING
    # ========================================================

    def backward_chain(self, goal):

        reasoning_steps = []

        visited = set()

        def prove(target):

            # ------------------------------------------------
            # Already known?
            # ------------------------------------------------

            if target in self.facts:

                reasoning_steps.append(
                    f"FACT FOUND: {target}"
                )

                return True


            # ------------------------------------------------
            # Prevent circular reasoning
            # ------------------------------------------------

            if target in visited:

                return False

            visited.add(target)

            # ------------------------------------------------
            # Search for rules that conclude the target
            # ------------------------------------------------

            matching_rules = []

            for rule in self.rules:

                if rule["conclusion"] == target:

                    matching_rules.append(rule)


            # ------------------------------------------------
            # No rule can prove target
            # ------------------------------------------------

            if not matching_rules:

                reasoning_steps.append(
                    f"NO RULE FOUND: {target}"
                )

                return False


            # ------------------------------------------------
            # Try each matching rule
            # ------------------------------------------------

            for rule in matching_rules:

                conditions = rule["conditions"]

                reasoning_steps.append(
                    f"TRY RULE: {conditions} -> {target}"
                )

                all_conditions_proved = True

                for condition in conditions:

                    if not prove(condition):

                        all_conditions_proved = False

                        break


                if all_conditions_proved:

                    reasoning_steps.append(
                        f"GOAL SUPPORTED: {target}"
                    )

                    return True


            reasoning_steps.append(
                f"GOAL NOT PROVED: {target}"
            )

            return False


        result = prove(goal)

        return result, reasoning_steps


    # ========================================================
    # GET ALL FACTS
    # ========================================================

    def get_facts(self):

        return sorted(self.facts)


    # ========================================================
    # GET ALL RULES
    # ========================================================

    def get_rules(self):

        return self.rules


# ============================================================
# TEST KNOWLEDGE BASE
# ============================================================

def test_knowledge_base():

    kb = KnowledgeBase()

    # --------------------------------------------------------
    # Initial facts
    # --------------------------------------------------------

    kb.add_fact("player_alive")
    kb.add_fact("treasure_exists")
    kb.add_fact("goal_exists")

    # --------------------------------------------------------
    # Rules
    # --------------------------------------------------------

    kb.add_rule(
        ["player_alive"],
        "can_explore"
    )

    kb.add_rule(
        ["treasure_exists"],
        "treasure_available"
    )

    kb.add_rule(
        ["goal_exists"],
        "goal_available"
    )

    kb.add_rule(
        ["treasure_found"],
        "has_treasure"
    )

    kb.add_rule(
        ["has_treasure"],
        "seek_goal"
    )

    kb.add_rule(
        ["has_treasure", "goal_reached"],
        "mission_complete"
    )

    # --------------------------------------------------------
    # FORWARD CHAINING
    # --------------------------------------------------------

    forward_steps = kb.forward_chain()

    print()
    print("==============================================")
    print("       COGNITIVE QUEST - KNOWLEDGE BASE")
    print("==============================================")

    print()
    print("FORWARD CHAINING")
    print("----------------------------------------------")

    for number, step in enumerate(
        forward_steps,
        start=1
    ):

        print(
            f"{number}. {step}"
        )

    print()
    print("KNOWN FACTS")
    print("----------------------------------------------")

    for fact in kb.get_facts():

        print(
            f"- {fact}"
        )

    # --------------------------------------------------------
    # BACKWARD CHAINING
    # --------------------------------------------------------

    print()
    print("BACKWARD CHAINING")
    print("----------------------------------------------")

    goal = "mission_complete"

    result, backward_steps = (
        kb.backward_chain(goal)
    )

    print(
        f"Goal: {goal}"
    )

    print()

    for number, step in enumerate(
        backward_steps,
        start=1
    ):

        print(
            f"{number}. {step}"
        )

    print()

    if result:

        print(
            "RESULT: Goal can be proved."
        )

    else:

        print(
            "RESULT: Goal cannot currently be proved."
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    test_knowledge_base()