# ============================================================
# COGNITIVE QUEST
# AI DECISION / EVENT LOG
# ============================================================

class DecisionLog:

    def __init__(self, max_entries=12):
        self.entries = []
        self.max_entries = max_entries

    def add(self, message):
        self.entries.append(message)

        if len(self.entries) > self.max_entries:
            self.entries.pop(0)

    def clear(self):
        self.entries = []

    def get_entries(self):
        return self.entries

    def latest(self):
        if len(self.entries) == 0:
            return "No AI decisions yet."

        return self.entries[-1]


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    log = DecisionLog()

    log.add("BFS search executed.")
    log.add("Enemy selected Minimax move.")
    log.add("Difficulty changed to Medium.")

    print("AI DECISION LOG")
    print("----------------")

    for entry in log.get_entries():
        print(entry)

    print()
    print("Latest:", log.latest())