# ============================================================
# COGNITIVE QUEST
# INTELLIGENT ENEMY AI
#
# A* + MINIMAX + DECISION EXPLANATION
# ============================================================

import time

from ai.search import astar
from ai.minimax import find_best_move


class Enemy:

    def __init__(self, start_position):

        # ----------------------------------------------------
        # POSITION
        # ----------------------------------------------------

        self.row = start_position[0]
        self.col = start_position[1]

        # ----------------------------------------------------
        # A* INFORMATION
        # ----------------------------------------------------

        self.path = []
        self.target = None
        self.explored = []

        # ----------------------------------------------------
        # MOVEMENT
        # ----------------------------------------------------

        self.last_move_time = time.time()

        self.move_delay = 0.8

        self.steps_taken = 0

        self.active = True

        # ----------------------------------------------------
        # AI INFORMATION
        # ----------------------------------------------------

        self.ai_mode = "A* + Minimax"

        self.minimax_score = 0

        self.minimax_depth = 2

        self.decision = "Waiting"

        self.best_move = (
            self.row,
            self.col
        )

        self.reason = "Waiting for player."


    # ========================================================
    # GET POSITION
    # ========================================================

    def get_position(self):

        return (
            self.row,
            self.col
        )


    # ========================================================
    # A* PATH CALCULATION
    # ========================================================

    def calculate_path(
        self,
        game_map,
        target
    ):

        self.target = target

        start = (
            self.row,
            self.col
        )

        (
            self.path,
            self.explored
        ) = astar(
            game_map,
            start,
            target
        )

        return (
            self.path,
            self.explored
        )


    # ========================================================
    # MINIMAX DECISION
    # ========================================================

    def calculate_minimax_move(
        self,
        game_map,
        player_position,
        treasure_position,
        goal_position,
        depth=2
    ):

        enemy_position = (
            self.row,
            self.col
        )

        self.minimax_depth = depth

        (
            best_move,
            score
        ) = find_best_move(
            enemy_position,
            player_position,
            game_map,
            treasure_position,
            goal_position,
            depth=depth
        )

        self.minimax_score = score

        self.best_move = best_move

        return best_move


    # ========================================================
    # UPDATE ENEMY
    # ========================================================

    def update(
        self,
        game_map,
        player_position,
        treasure_position,
        goal_position,
        minimax_depth=2
    ):

        if not self.active:

            return None

        current_time = time.time()

        # ----------------------------------------------------
        # MOVEMENT DELAY
        # ----------------------------------------------------

        if (
            current_time
            -
            self.last_move_time
            <
            self.move_delay
        ):

            return None

        self.last_move_time = current_time

        # ----------------------------------------------------
        # A* PATH
        # ----------------------------------------------------

        (
            path,
            explored
        ) = self.calculate_path(
            game_map,
            player_position
        )

        # ----------------------------------------------------
        # MINIMAX
        # ----------------------------------------------------

        best_move = self.calculate_minimax_move(
            game_map,
            player_position,
            treasure_position,
            goal_position,
            minimax_depth
        )

        # ----------------------------------------------------
        # DECISION EXPLANATION
        # ----------------------------------------------------

        if path:

            path_length = len(path)

        else:

            path_length = 0

        current_position = (
            self.row,
            self.col
        )

        # ----------------------------------------------------
        # MOVE
        # ----------------------------------------------------

        if best_move != current_position:

            self.row = best_move[0]
            self.col = best_move[1]

            self.steps_taken += 1

            self.ai_mode = "A* + Minimax"

            self.decision = "Strategic move"

            self.reason = (
                "Moved toward player"
                " using Minimax."
            )

        else:

            self.decision = "No useful move"

            self.reason = (
                "No better move found."
            )

        return explored


    # ========================================================
    # RESET
    # ========================================================

    def reset(
        self,
        start_position
    ):

        self.row = start_position[0]

        self.col = start_position[1]

        self.path = []

        self.target = None

        self.explored = []

        self.last_move_time = time.time()

        self.move_delay = 0.8

        self.steps_taken = 0

        self.active = True

        self.ai_mode = "A* + Minimax"

        self.minimax_score = 0

        self.minimax_depth = 2

        self.decision = "Waiting"

        self.best_move = (
            self.row,
            self.col
        )

        self.reason = (
            "Waiting for player."
        )