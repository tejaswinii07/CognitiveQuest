# ============================================================
# COGNITIVE QUEST - CSP MODULE
# Constraint Satisfaction Problem
# ============================================================


def is_valid_assignment(assignment):
    """
    Check whether the current assignment satisfies
    all CSP constraints.
    """

    # A < B
    if "A" in assignment and "B" in assignment:
        if assignment["A"] >= assignment["B"]:
            return False

    # C > A
    if "A" in assignment and "C" in assignment:
        if assignment["C"] <= assignment["A"]:
            return False

    # D > C
    if "C" in assignment and "D" in assignment:
        if assignment["D"] <= assignment["C"]:
            return False

    # B != C
    if "B" in assignment and "C" in assignment:
        if assignment["B"] == assignment["C"]:
            return False

    # All values must be different
    values = list(assignment.values())

    if len(values) != len(set(values)):
        return False

    return True


def validate_player_solution(assignment):
    """
    Validate the complete solution entered by the player.

    Returns:
        (True, message)  if correct
        (False, message) if incorrect
    """

    required = ["A", "B", "C", "D"]

    # Check that all variables have values
    for variable in required:
        if variable not in assignment:
            return False, f"{variable} has not been assigned."

    # Check range
    for variable in required:
        value = assignment[variable]

        if value not in [1, 2, 3, 4]:
            return False, f"{variable} must contain a value from 1 to 4."

    # All values must be different
    values = [assignment["A"],
              assignment["B"],
              assignment["C"],
              assignment["D"]]

    if len(set(values)) != 4:
        return False, "Each number from 1 to 4 can be used only once."

    # Individual constraints

    if assignment["A"] >= assignment["B"]:
        return False, "Constraint violated: A must be less than B."

    if assignment["C"] <= assignment["A"]:
        return False, "Constraint violated: C must be greater than A."

    if assignment["D"] <= assignment["C"]:
        return False, "Constraint violated: D must be greater than C."

    if assignment["B"] == assignment["C"]:
        return False, "Constraint violated: B and C must be different."

    return True, "All constraints satisfied!"


def solve_csp():
    """
    Solve the CSP using backtracking.

    Variables:
        A, B, C, D

    Domain:
        1, 2, 3, 4

    Constraints:
        A < B
        C > A
        D > C
        B != C
        All values different
    """

    variables = ["A", "B", "C", "D"]
    domain = [1, 2, 3, 4]

    assignment = {}
    steps = []
    attempts = 0

    def backtrack():
        nonlocal attempts

        # Complete assignment
        if len(assignment) == len(variables):
            return assignment.copy()

        variable = variables[len(assignment)]

        for value in domain:

            attempts += 1

            assignment[variable] = value

            steps.append(
                f"Try {variable} = {value}"
            )

            if is_valid_assignment(assignment):

                steps.append(
                    f"Valid: {variable} = {value}"
                )

                result = backtrack()

                if result is not None:
                    return result

            else:

                steps.append(
                    f"Invalid: {variable} = {value}"
                )

            steps.append(
                f"Backtrack from {variable} = {value}"
            )

            del assignment[variable]

        return None

    solution = backtrack()

    return solution, steps, attempts


def display_result():
    """
    Simple console demonstration.
    """

    solution, steps, attempts = solve_csp()

    print("\n===== CSP SOLVER =====")

    if solution:
        print("Solution:", solution)

    print("Attempts:", attempts)

    print("\nBacktracking steps:")

    for step in steps:
        print(step)


if __name__ == "__main__":
    display_result()