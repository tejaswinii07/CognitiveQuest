# ============================================================
# COGNITIVE QUEST
# MINIMAX AI
# Strategic Enemy Decision Making
# ============================================================


# ============================================================
# HEURISTIC EVALUATION
# ============================================================

def evaluate_state(
    enemy_position,
    player_position,
    treasure_position,
    goal_position
):
    """
    Evaluate the current game state.

    Higher score = better state for enemy.

    The enemy wants to:
    - Get closer to the player.
    - Avoid moving unnecessarily far away.
    """

    enemy_row, enemy_col = enemy_position

    player_row, player_col = player_position

    # Manhattan distance to player

    player_distance = (
        abs(enemy_row - player_row)
        +
        abs(enemy_col - player_col)
    )

    # Manhattan distance to treasure

    treasure_distance = (
        abs(enemy_row - treasure_position[0])
        +
        abs(enemy_col - treasure_position[1])
    )

    # Manhattan distance to goal

    goal_distance = (
        abs(enemy_row - goal_position[0])
        +
        abs(enemy_col - goal_position[1])
    )

    # Enemy prefers smaller distance to player.

    score = (
        -player_distance * 10
        -treasure_distance
        -goal_distance
    )

    return score


# ============================================================
# GET POSSIBLE MOVES
# ============================================================

def get_possible_moves(
    position,
    game_map
):

    row, col = position

    directions = [

        (-1, 0),   # Up
        (1, 0),    # Down
        (0, -1),   # Left
        (0, 1)     # Right

    ]

    possible_moves = []

    for row_change, col_change in directions:

        new_row = row + row_change

        new_col = col + col_change

        # Check boundaries

        if new_row < 0:
            continue

        if new_row >= len(game_map):
            continue

        if new_col < 0:
            continue

        if new_col >= len(game_map[0]):
            continue

        # Ignore walls

        if game_map[new_row][new_col] == 1:
            continue

        possible_moves.append(
            (new_row, new_col)
        )

    return possible_moves


# ============================================================
# MINIMAX
# ============================================================

def minimax(
    enemy_position,
    player_position,
    game_map,
    treasure_position,
    goal_position,
    depth,
    maximizing_player
):
    """
    Minimax decision algorithm.

    The enemy is the maximizing player.

    The player is treated as the minimizing player.
    """

    # Base case

    if depth == 0:

        return evaluate_state(
            enemy_position,
            player_position,
            treasure_position,
            goal_position
        )

    # ========================================================
    # ENEMY TURN
    # ========================================================

    if maximizing_player:

        best_score = float("-inf")

        possible_moves = get_possible_moves(
            enemy_position,
            game_map
        )

        if not possible_moves:

            return evaluate_state(
                enemy_position,
                player_position,
                treasure_position,
                goal_position
            )

        for move in possible_moves:

            score = minimax(
                move,
                player_position,
                game_map,
                treasure_position,
                goal_position,
                depth - 1,
                False
            )

            best_score = max(
                best_score,
                score
            )

        return best_score

    # ========================================================
    # PLAYER TURN
    # ========================================================

    else:

        best_score = float("inf")

        possible_moves = get_possible_moves(
            player_position,
            game_map
        )

        if not possible_moves:

            return evaluate_state(
                enemy_position,
                player_position,
                treasure_position,
                goal_position
            )

        for move in possible_moves:

            score = minimax(
                enemy_position,
                move,
                game_map,
                treasure_position,
                goal_position,
                depth - 1,
                True
            )

            best_score = min(
                best_score,
                score
            )

        return best_score


# ============================================================
# FIND BEST ENEMY MOVE
# ============================================================

def find_best_move(
    enemy_position,
    player_position,
    game_map,
    treasure_position,
    goal_position,
    depth=2
):
    """
    Calculate the best next move for the enemy.
    """

    possible_moves = get_possible_moves(
        enemy_position,
        game_map
    )

    if not possible_moves:

        return enemy_position, 0

    best_move = possible_moves[0]

    best_score = float("-inf")

    # --------------------------------------------------------
    # Evaluate every possible move
    # --------------------------------------------------------

    for move in possible_moves:

        score = minimax(
            move,
            player_position,
            game_map,
            treasure_position,
            goal_position,
            depth - 1,
            False
        )

        if score > best_score:

            best_score = score

            best_move = move

    return best_move, best_score


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_map = [

        [0, 0, 0, 0],

        [0, 1, 1, 0],

        [0, 0, 0, 0],

        [0, 0, 0, 0]

    ]

    enemy = (3, 0)

    player = (0, 3)

    treasure = (2, 2)

    goal = (3, 3)

    best_move, score = find_best_move(

        enemy,

        player,

        test_map,

        treasure,

        goal,

        depth=2

    )

    print()
    print("======================================")
    print("        COGNITIVE QUEST")
    print("          MINIMAX TEST")
    print("======================================")
    print()

    print(
        "Enemy position:",
        enemy
    )

    print(
        "Player position:",
        player
    )

    print(
        "Best enemy move:",
        best_move
    )

    print(
        "Minimax score:",
        score
    )

    print()