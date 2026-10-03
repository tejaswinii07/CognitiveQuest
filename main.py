import pygame
import sys
import time

from ai.search import bfs, dfs, astar
from ai.csp import solve_csp, validate_player_solution
from ai.knowledge_base import KnowledgeBase
from ai.enemy import Enemy
from ai.adaptive import AdaptiveDifficulty
from ai.decision_log import DecisionLog


# ============================================================
# INITIALIZATION
# ============================================================

pygame.init()

pygame.display.set_caption("Cognitive Quest")

info = pygame.display.Info()

SCREEN_WIDTH = min(info.current_w, 1500)
SCREEN_HEIGHT = min(info.current_h, 900)

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

clock = pygame.time.Clock()


# ============================================================
# COLORS
# ============================================================

BG = (12, 16, 25)
PANEL = (22, 28, 42)
PANEL_LIGHT = (31, 39, 57)

WHITE = (240, 243, 250)
GRAY = (160, 170, 190)

BLUE = (70, 150, 255)
CYAN = (60, 220, 220)

GREEN = (70, 210, 130)
YELLOW = (240, 200, 70)
RED = (235, 80, 90)

PURPLE = (160, 100, 240)
ORANGE = (240, 145, 70)

WALL = (55, 63, 82)
FLOOR = (27, 34, 49)

SEARCH_COLOR = (70, 130, 200)
PATH_COLOR = (100, 220, 150)


# ============================================================
# FONTS
# ============================================================

FONT_TITLE = pygame.font.SysFont("segoeui", 40, bold=True)
FONT_BIG = pygame.font.SysFont("segoeui", 28, bold=True)
FONT_MEDIUM = pygame.font.SysFont("segoeui", 21, bold=True)
FONT_NORMAL = pygame.font.SysFont("segoeui", 18)
FONT_SMALL = pygame.font.SysFont("segoeui", 15)
FONT_TINY = pygame.font.SysFont("segoeui", 13)


# ============================================================
# LEVEL DATA
# ============================================================

LEVELS = [

    {
        "name": "The Forgotten Corridor",

        "map": [
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 5, 4, 2],
            [0, 0, 0, 1, 0, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 0, 0, 3]
        ],

        "player": (0, 0),
        "enemy": (4, 1),
        "key": (2, 6),
        "door": (2, 7),
        "treasure": (2, 8),
        "goal": (4, 8)
    },

    {
        "name": "The Security Wing",

        "map": [
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 5, 1, 0],
            [1, 1, 1, 1, 1, 1, 4, 1, 0],
            [0, 0, 0, 0, 0, 0, 2, 0, 3]
        ],

        "player": (0, 0),
        "enemy": (4, 3),
        "key": (2, 6),
        "door": (3, 6),
        "treasure": (4, 6),
        "goal": (4, 8)
    },

    {
        "name": "The Final Fortress",

        "map": [
            [0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 5, 1, 0],
            [0, 1, 1, 1, 1, 1, 4, 1, 0],
            [0, 0, 0, 0, 0, 0, 2, 0, 3]
        ],

        "player": (0, 0),
        "enemy": (4, 2),
        "key": (2, 6),
        "door": (3, 6),
        "treasure": (4, 6),
        "goal": (4, 8)
    }
]


# ============================================================
# GAME STATE
# ============================================================

current_level = 0

game_map = []
level_name = ""

player_position = (0, 0)
enemy = None

key_position = None
door_position = None
treasure_position = None
goal_position = None

key_collected = False
door_open = False
treasure_collected = False

player_health = 100
move_count = 0
score = 0

game_over = False
level_complete = False
mission_complete = False

message = "Find the key."

current_search_name = "None"
current_search_path = []
current_search_explored = []

game_state = "MENU"

# Main-menu selection.
# The mouse can highlight/click buttons, while the keyboard
# can still use UP/DOWN + ENTER.
menu_selected = 0

# AI Analysis screen state.
analysis_selected = 0


# ============================================================
# CSP STATE
# ============================================================

csp_puzzle_active = False
csp_solved = False

csp_values = {
    "A": "",
    "B": "",
    "C": "",
    "D": ""
}

csp_selected = "A"

csp_message = "Enter values from 1 to 4."

csp_message_good = False

csp_solution = None
csp_steps = []
csp_attempts = 0

show_csp_ai_solution = False


# ============================================================
# AI STATE
# ============================================================

knowledge_base = KnowledgeBase()

adaptive = AdaptiveDifficulty()

decision_log = DecisionLog(max_entries=8)

knowledge_reasoning = []
backward_reasoning = []


# ============================================================
# LEVEL LOADING
# ============================================================

def load_level(index):

    global current_level
    global game_map
    global level_name

    global player_position
    global enemy

    global key_position
    global door_position
    global treasure_position
    global goal_position

    global key_collected
    global door_open
    global treasure_collected

    global player_health
    global move_count

    global game_over
    global level_complete

    global current_search_name
    global current_search_path
    global current_search_explored

    global csp_puzzle_active
    global csp_solved
    global csp_values
    global csp_selected
    global csp_message
    global csp_solution
    global csp_steps
    global csp_attempts
    global show_csp_ai_solution

    current_level = index

    level = LEVELS[index]

    game_map = [row[:] for row in level["map"]]

    level_name = level["name"]

    player_position = level["player"]

    enemy = Enemy(level["enemy"])

    key_position = level["key"]
    door_position = level["door"]
    treasure_position = level["treasure"]
    goal_position = level["goal"]

    key_collected = False
    door_open = False
    treasure_collected = False

    player_health = 100
    move_count = 0

    game_over = False
    level_complete = False

    current_search_name = "None"
    current_search_path = []
    current_search_explored = []

    csp_puzzle_active = False
    csp_solved = False

    csp_values = {
        "A": "",
        "B": "",
        "C": "",
        "D": ""
    }

    csp_selected = "A"

    csp_message = "Enter values from 1 to 4."

    csp_solution = None
    csp_steps = []
    csp_attempts = 0

    show_csp_ai_solution = False

    decision_log.clear()

    initialize_knowledge()

    decision_log.add(
        f"Level {current_level + 1} started."
    )


# ============================================================
# KNOWLEDGE BASE
# ============================================================

def initialize_knowledge():

    global knowledge_base

    knowledge_base = KnowledgeBase()

    knowledge_base.add_fact("player_alive")
    knowledge_base.add_fact("key_exists")
    knowledge_base.add_fact("treasure_exists")
    knowledge_base.add_fact("goal_exists")

    knowledge_base.add_rule(
        ["player_alive"],
        "can_explore"
    )

    knowledge_base.add_rule(
        ["key_exists"],
        "key_available"
    )

    knowledge_base.add_rule(
        ["key_found"],
        "security_system_active"
    )

    knowledge_base.add_rule(
        ["csp_solved"],
        "door_can_open"
    )

    knowledge_base.add_rule(
        ["door_open"],
        "treasure_available"
    )

    knowledge_base.add_rule(
        ["treasure_exists"],
        "treasure_available"
    )

    knowledge_base.add_rule(
        ["treasure_found"],
        "has_treasure"
    )

    knowledge_base.add_rule(
        ["has_treasure"],
        "seek_goal"
    )

    knowledge_base.add_rule(
        ["enemy_near"],
        "danger_detected"
    )

    knowledge_base.add_rule(
        ["danger_detected"],
        "avoid_enemy"
    )


def update_knowledge():

    global knowledge_reasoning
    global backward_reasoning

    if key_collected:
        knowledge_base.add_fact("key_found")

    if csp_solved:
        knowledge_base.add_fact("csp_solved")

    if door_open:
        knowledge_base.add_fact("door_open")

    if treasure_collected:
        knowledge_base.add_fact("treasure_found")

    enemy_distance = abs(
        enemy.row - player_position[0]
    ) + abs(
        enemy.col - player_position[1]
    )

    if enemy_distance <= 3:
        knowledge_base.add_fact("enemy_near")
    else:
        knowledge_base.remove_fact("enemy_near")

    knowledge_reasoning = knowledge_base.forward_chain()

    result, backward_reasoning = knowledge_base.backward_chain(
        "seek_goal"
    )


# ============================================================
# AI MAP
# ============================================================

def get_ai_map():

    ai_map = [row[:] for row in game_map]

    # Closed door behaves like a wall
    if not door_open:
        r, c = door_position
        ai_map[r][c] = 1

    return ai_map


# ============================================================
# SCORING
# ============================================================

def add_score(points, reason):

    global score

    score += points

    decision_log.add(
        f"Score +{points}: {reason}"
    )


# ============================================================
# PLAYER MOVEMENT
# ============================================================

def move_player(dr, dc):

    global player_position
    global move_count

    global key_collected
    global treasure_collected

    global message
    global game_over

    if game_over or level_complete:
        return

    new_row = player_position[0] + dr
    new_col = player_position[1] + dc

    rows = len(game_map)
    cols = len(game_map[0])

    if new_row < 0 or new_row >= rows:
        return

    if new_col < 0 or new_col >= cols:
        return

    # --------------------------------------------------------
    # CLOSED DOOR
    # --------------------------------------------------------

    if (new_row, new_col) == door_position and not door_open:

        if not key_collected:
            message = "LOCKED: Find the security key first."
            decision_log.add("Player attempted locked door.")
            return

        open_csp_puzzle()

        return

    # --------------------------------------------------------
    # WALL
    # --------------------------------------------------------

    if game_map[new_row][new_col] == 1:

        message = "Blocked by a wall."

        return

    # --------------------------------------------------------
    # MOVE
    # --------------------------------------------------------

    player_position = (new_row, new_col)

    move_count += 1

    # --------------------------------------------------------
    # KEY
    # --------------------------------------------------------

    if player_position == key_position and not key_collected:

        key_collected = True

        add_score(100, "Security key collected")

        message = "Security key collected! +100 points"

        decision_log.add(
            "Key collected. Security system activated."
        )

        update_knowledge()

    # --------------------------------------------------------
    # TREASURE
    # --------------------------------------------------------

    if (
        player_position == treasure_position
        and door_open
        and not treasure_collected
    ):

        treasure_collected = True

        add_score(300, "Treasure collected")

        message = "Treasure collected! +300 points. Reach the goal."

        decision_log.add(
            "Treasure collected. Goal objective activated."
        )

        update_knowledge()

    # --------------------------------------------------------
    # GOAL
    # --------------------------------------------------------

    if (
        player_position == goal_position
        and treasure_collected
    ):

        complete_level()

    update_knowledge()


# ============================================================
# CSP PUZZLE
# ============================================================

def open_csp_puzzle():

    global csp_puzzle_active
    global csp_message
    global csp_values
    global csp_selected
    global show_csp_ai_solution

    if not key_collected:
        return

    csp_puzzle_active = True

    csp_values = {
        "A": "",
        "B": "",
        "C": "",
        "D": ""
    }

    csp_selected = "A"

    csp_message = "Enter values from 1 to 4."

    show_csp_ai_solution = False

    decision_log.add(
        "Security door reached. CSP puzzle activated."
    )


def solve_player_csp():

    global csp_solved
    global door_open
    global csp_puzzle_active

    global csp_message
    global csp_message_good

    global csp_solution
    global csp_steps
    global csp_attempts

    global show_csp_ai_solution
    global message

    # Check that every field is filled
    for variable in ["A", "B", "C", "D"]:

        if csp_values[variable] == "":

            csp_message = (
                f"Please enter a value for {variable}."
            )

            csp_message_good = False

            return

    # Convert values
    try:

        assignment = {
            "A": int(csp_values["A"]),
            "B": int(csp_values["B"]),
            "C": int(csp_values["C"]),
            "D": int(csp_values["D"])
        }

    except ValueError:

        csp_message = "Only numbers 1 to 4 are allowed."

        csp_message_good = False

        return

    # Validate player solution
    valid, result = validate_player_solution(
        assignment
    )

    if valid:

        csp_solved = True
        door_open = True

        add_score(200, "CSP security puzzle solved")

        csp_message = (
            "✓ Correct! All constraints satisfied."
        )

        csp_message_good = True

        message = (
            "Security system solved! Door unlocked."
        )

        # Run AI solver as well
        (
            csp_solution,
            csp_steps,
            csp_attempts
        ) = solve_csp()

        show_csp_ai_solution = True

        decision_log.add(
            "CSP solved. Security door unlocked."
        )

        update_knowledge()

        # Immediately return to the map after a correct solution.
        # The player should NOT need to press ENTER a second time.
        csp_puzzle_active = False

    else:

        csp_message = "✗ " + result

        csp_message_good = False

        decision_log.add(
            "Incorrect CSP assignment. Try again."
        )


# ============================================================
# ENEMY UPDATE
# ============================================================

def update_enemy():

    global player_health
    global score
    global message
    global current_search_name

    if game_over or level_complete:
        return

    if csp_puzzle_active:
        return

    distance = abs(
        enemy.row - player_position[0]
    ) + abs(
        enemy.col - player_position[1]
    )

    adaptive.calculate_difficulty(
        player_health,
        move_count,
        treasure_collected,
        distance
    )

    enemy.move_delay = adaptive.get_enemy_delay()

    explored = enemy.update(
        get_ai_map(),
        player_position,
        treasure_position,
        goal_position,
        adaptive.get_minimax_depth()
    )

    if explored is not None:

        current_search_name = "A*"

        decision_log.add(
            f"Enemy used A* + Minimax. "
            f"Depth {adaptive.get_minimax_depth()}."
        )

    # Enemy catches player
    if enemy.get_position() == player_position:

        player_health -= 20

        score_loss = min(100, score)
        score -= score_loss

        message = (
            "The enemy caught you! "
            f"Health: {player_health}"
        )

        decision_log.add(
            f"Enemy reached player. Health reduced. Score -{score_loss}."
        )

        # Move the enemy away after a hit so it does not remain
        # on the player's cell and repeatedly damage the player.
        if player_health > 0:

            ai_map = get_ai_map()

            possible_cells = [
                (enemy.row - 1, enemy.col),
                (enemy.row + 1, enemy.col),
                (enemy.row, enemy.col - 1),
                (enemy.row, enemy.col + 1)
            ]

            for new_row, new_col in possible_cells:

                if (
                    0 <= new_row < len(ai_map)
                    and 0 <= new_col < len(ai_map[0])
                    and ai_map[new_row][new_col] == 0
                    and (new_row, new_col) != player_position
                ):
                    enemy.row = new_row
                    enemy.col = new_col
                    break

            enemy.last_move_time = time.time()

        else:

            end_game()


# ============================================================
# SEARCH DEMONSTRATIONS
# ============================================================

def run_bfs():

    global current_search_name
    global current_search_path
    global current_search_explored

    path, explored = bfs(
        get_ai_map(),
        player_position,
        goal_position
    )

    current_search_name = "BFS"
    current_search_path = path
    current_search_explored = explored

    decision_log.add(
        f"BFS analyzed {len(explored)} cells."
    )


def run_dfs():

    global current_search_name
    global current_search_path
    global current_search_explored

    path, explored = dfs(
        get_ai_map(),
        player_position,
        goal_position
    )

    current_search_name = "DFS"
    current_search_path = path
    current_search_explored = explored

    decision_log.add(
        f"DFS analyzed {len(explored)} cells."
    )


def run_astar():

    global current_search_name
    global current_search_path
    global current_search_explored

    path, explored = astar(
        get_ai_map(),
        player_position,
        goal_position
    )

    current_search_name = "A*"
    current_search_path = path
    current_search_explored = explored

    decision_log.add(
        f"A* analyzed {len(explored)} cells."
    )


# ============================================================
# GAME PROGRESSION
# ============================================================

def complete_level():

    global level_complete
    global message

    level_complete = True

    add_score(250, f"Level {current_level + 1} completed")

    message = (
        f"Level {current_level + 1} complete! +250 points"
    )

    decision_log.add(
        f"Level {current_level + 1} completed."
    )


def advance_level():

    global mission_complete
    global game_state

    if current_level < len(LEVELS) - 1:

        load_level(current_level + 1)

    else:

        mission_complete = True
        game_state = "MISSION_COMPLETE"


def end_game():

    global game_over
    global game_state

    game_over = True

    game_state = "GAME_OVER"

    decision_log.add(
        "Player health reached zero."
    )


# ============================================================
# DRAWING HELPERS
# ============================================================

def draw_text(
    text,
    x,
    y,
    font=FONT_NORMAL,
    color=WHITE
):

    surface = font.render(
        str(text),
        True,
        color
    )

    screen.blit(surface, (x, y))


def draw_centered_text(
    text,
    center_x,
    y,
    font=FONT_NORMAL,
    color=WHITE
):

    surface = font.render(
        str(text),
        True,
        color
    )

    rect = surface.get_rect(
        centerx=center_x,
        y=y
    )

    screen.blit(surface, rect)


def draw_panel(rect):

    pygame.draw.rect(
        screen,
        PANEL,
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        PANEL_LIGHT,
        rect,
        1,
        border_radius=12
    )


# ============================================================
# GAME LAYOUT
# ============================================================

def get_layout():

    left_margin = 30

    top = 125

    panel_width = 300

    right_margin = 30

    available_width = (
        SCREEN_WIDTH
        - left_margin
        - right_margin
        - panel_width
        - 30
    )

    map_width = available_width

    map_height = SCREEN_HEIGHT - 220

    rows = len(game_map)
    cols = len(game_map[0])

    cell_size = min(
        map_width // cols,
        map_height // rows
    )

    grid_width = cell_size * cols
    grid_height = cell_size * rows

    map_x = left_margin

    map_y = top + (
        map_height - grid_height
    ) // 2

    panel_x = (
        map_x
        + grid_width
        + 25
    )

    return (
        map_x,
        map_y,
        cell_size,
        panel_x
    )


# ============================================================
# DRAW MAP
# ============================================================

def draw_map():

    map_x, map_y, cell_size, panel_x = get_layout()

    # Base cells
    for r, row in enumerate(game_map):

        for c, value in enumerate(row):

            x = map_x + c * cell_size
            y = map_y + r * cell_size

            if value == 1:

                pygame.draw.rect(
                    screen,
                    WALL,
                    (x + 2, y + 2,
                     cell_size - 4,
                     cell_size - 4),
                    border_radius=5
                )

            else:

                pygame.draw.rect(
                    screen,
                    FLOOR,
                    (x + 2, y + 2,
                     cell_size - 4,
                     cell_size - 4),
                    border_radius=5
                )

    # Search visualization is drawn AFTER the cells so it is visible.
    for r, c in current_search_explored:

        x = map_x + c * cell_size
        y = map_y + r * cell_size

        pygame.draw.rect(
            screen,
            SEARCH_COLOR,
            (x + 3, y + 3,
             cell_size - 6,
             cell_size - 6),
            border_radius=5
        )

    # Search path
    for r, c in current_search_path:

        x = map_x + c * cell_size
        y = map_y + r * cell_size

        pygame.draw.rect(
            screen,
            PATH_COLOR,
            (x + cell_size // 3,
             y + cell_size // 3,
             cell_size // 3,
             cell_size // 3),
            border_radius=4
        )

    # Door
    dr, dc = door_position

    if not door_open:

        x = map_x + dc * cell_size
        y = map_y + dr * cell_size

        pygame.draw.rect(
            screen,
            RED,
            (x + 8, y + 8,
             cell_size - 16,
             cell_size - 16),
            border_radius=8
        )

        draw_centered_text(
            "LOCK",
            x + cell_size // 2,
            y + cell_size // 2 - 10,
            FONT_SMALL,
            WHITE
        )

    else:

        x = map_x + dc * cell_size
        y = map_y + dr * cell_size

        pygame.draw.rect(
            screen,
            GREEN,
            (x + 8, y + 8,
             cell_size - 16,
             cell_size - 16),
            border_radius=8
        )

        draw_centered_text(
            "OPEN",
            x + cell_size // 2,
            y + cell_size // 2 - 10,
            FONT_SMALL,
            WHITE
        )

    # Key
    if not key_collected:

        r, c = key_position

        x = map_x + c * cell_size
        y = map_y + r * cell_size

        pygame.draw.circle(
            screen,
            YELLOW,
            (
                x + cell_size // 2,
                y + cell_size // 2
            ),
            max(6, cell_size // 6)
        )

        draw_centered_text(
            "K",
            x + cell_size // 2,
            y + cell_size // 2 - 10,
            FONT_SMALL,
            BG
        )

    # Treasure
    if not treasure_collected:

        r, c = treasure_position

        x = map_x + c * cell_size
        y = map_y + r * cell_size

        pygame.draw.rect(
            screen,
            ORANGE,
            (
                x + cell_size // 4,
                y + cell_size // 3,
                cell_size // 2,
                cell_size // 3
            ),
            border_radius=5
        )

        draw_centered_text(
            "T",
            x + cell_size // 2,
            y + cell_size // 2 - 9,
            FONT_SMALL,
            WHITE
        )

    # Goal
    r, c = goal_position

    x = map_x + c * cell_size
    y = map_y + r * cell_size

    pygame.draw.circle(
        screen,
        PURPLE,
        (
            x + cell_size // 2,
            y + cell_size // 2
        ),
        max(8, cell_size // 4),
        3
    )

    draw_centered_text(
        "G",
        x + cell_size // 2,
        y + cell_size // 2 - 10,
        FONT_SMALL,
        WHITE
    )

    # Player
    r, c = player_position

    x = map_x + c * cell_size
    y = map_y + r * cell_size

    pygame.draw.circle(
        screen,
        CYAN,
        (
            x + cell_size // 2,
            y + cell_size // 2
        ),
        max(10, cell_size // 3)
    )

    draw_centered_text(
        "P",
        x + cell_size // 2,
        y + cell_size // 2 - 10,
        FONT_SMALL,
        BG
    )

    # Enemy
    er, ec = enemy.get_position()

    x = map_x + ec * cell_size
    y = map_y + er * cell_size

    pygame.draw.circle(
        screen,
        RED,
        (
            x + cell_size // 2,
            y + cell_size // 2
        ),
        max(10, cell_size // 3)
    )

    draw_centered_text(
        "E",
        x + cell_size // 2,
        y + cell_size // 2 - 10,
        FONT_SMALL,
        WHITE
    )


# ============================================================
# TOP HUD
# ============================================================

def draw_hud():

    pygame.draw.rect(
        screen,
        PANEL,
        (0, 0, SCREEN_WIDTH, 95)
    )

    draw_text(
        "COGNITIVE QUEST",
        30,
        16,
        FONT_BIG,
        WHITE
    )

    draw_text(
        f"LEVEL {current_level + 1}",
        30,
        55,
        FONT_SMALL,
        CYAN
    )

    draw_text(
        level_name,
        130,
        55,
        FONT_SMALL,
        GRAY
    )

    # Health
    draw_text(
        "HEALTH",
        SCREEN_WIDTH - 440,
        18,
        FONT_TINY,
        GRAY
    )

    pygame.draw.rect(
        screen,
        (50, 55, 70),
        (
            SCREEN_WIDTH - 440,
            42,
            110,
            12
        ),
        border_radius=6
    )

    pygame.draw.rect(
        screen,
        GREEN if player_health > 50 else RED,
        (
            SCREEN_WIDTH - 440,
            42,
            int(110 * player_health / 100),
            12
        ),
        border_radius=6
    )

    draw_text(
        str(player_health),
        SCREEN_WIDTH - 320,
        35,
        FONT_SMALL,
        WHITE
    )

    # Score
    draw_text(
        f"SCORE  {score}",
        SCREEN_WIDTH - 230,
        18,
        FONT_MEDIUM,
        YELLOW
    )

    # Moves
    draw_text(
        f"MOVES  {move_count}",
        SCREEN_WIDTH - 230,
        52,
        FONT_SMALL,
        WHITE
    )


# ============================================================
# OBJECTIVES PANEL
# ============================================================

def draw_objectives(panel_x):

    rect = pygame.Rect(
        panel_x,
        125,
        300,
        225
    )

    draw_panel(rect)

    draw_text(
        "MISSION",
        panel_x + 18,
        140,
        FONT_MEDIUM,
        WHITE
    )

    objectives = [
        (
            key_collected,
            "Find the security key"
        ),
        (
            door_open,
            "Unlock security door"
        ),
        (
            treasure_collected,
            "Collect the treasure"
        ),
        (
            level_complete,
            "Reach the goal"
        )
    ]

    y = 180

    for completed, text in objectives:

        symbol = "✓" if completed else "○"

        color = GREEN if completed else GRAY

        draw_text(
            symbol,
            panel_x + 20,
            y,
            FONT_NORMAL,
            color
        )

        draw_text(
            text,
            panel_x + 50,
            y,
            FONT_SMALL,
            WHITE if not completed else GREEN
        )

        y += 35

    # Current objective
    if not key_collected:
        objective = "Find the security key"
    elif not door_open:
        objective = "Reach the security door"
    elif not treasure_collected:
        objective = "Collect the treasure"
    else:
        objective = "Reach the goal"

    draw_text(
        "NOW",
        panel_x + 20,
        310,
        FONT_TINY,
        CYAN
    )

    draw_text(
        objective,
        panel_x + 60,
        308,
        FONT_TINY,
        WHITE
    )


# ============================================================
# AI PANEL
# ============================================================

def draw_ai_panel(panel_x):

    rect = pygame.Rect(
        panel_x,
        365,
        300,
        220
    )

    draw_panel(rect)

    draw_text(
        "AI STATUS",
        panel_x + 18,
        380,
        FONT_MEDIUM,
        WHITE
    )

    # Search algorithm currently shown/used
    draw_text(
        "Search",
        panel_x + 18,
        420,
        FONT_SMALL,
        GRAY
    )

    draw_text(
        current_search_name,
        panel_x + 115,
        420,
        FONT_SMALL,
        CYAN
    )

    draw_text(
        "Enemy",
        panel_x + 18,
        450,
        FONT_SMALL,
        GRAY
    )

    draw_text(
        "A* + Minimax",
        panel_x + 115,
        450,
        FONT_SMALL,
        CYAN
    )

    draw_text(
        "Decision",
        panel_x + 18,
        480,
        FONT_SMALL,
        GRAY
    )

    decision = enemy.decision
    if len(decision) > 22:
        decision = decision[:19] + "..."

    draw_text(
        decision,
        panel_x + 115,
        480,
        FONT_TINY,
        WHITE
    )

    draw_text(
        "Depth",
        panel_x + 18,
        510,
        FONT_SMALL,
        GRAY
    )

    draw_text(
        adaptive.get_minimax_depth(),
        panel_x + 115,
        510,
        FONT_SMALL,
        WHITE
    )

    draw_text(
        "Difficulty",
        panel_x + 18,
        540,
        FONT_SMALL,
        GRAY
    )

    draw_text(
        adaptive.get_status(),
        panel_x + 115,
        540,
        FONT_SMALL,
        YELLOW
    )



# ============================================================
# EVENT PANEL
# ============================================================

def draw_event_panel(panel_x):

    rect = pygame.Rect(
        panel_x,
        580,
        300,
        100
    )

    draw_panel(rect)

    draw_text(
        "CURRENT EVENT",
        panel_x + 18,
        595,
        FONT_SMALL,
        GRAY
    )

    # Word wrapping
    words = message.split()

    line = ""
    y = 625

    for word in words:

        test = line + word + " "

        if FONT_TINY.size(test)[0] > 260:

            draw_text(
                line,
                panel_x + 18,
                y,
                FONT_TINY,
                WHITE
            )

            y += 18

            line = word + " "

        else:

            line = test

    if line:

        draw_text(
            line,
            panel_x + 18,
            y,
            FONT_TINY,
            WHITE
        )


# ============================================================
# BOTTOM BAR
# ============================================================

def draw_bottom_bar():

    y = SCREEN_HEIGHT - 70

    pygame.draw.rect(
        screen,
        PANEL,
        (0, y, SCREEN_WIDTH, 70)
    )

    draw_text(
        "MOVE",
        30,
        y + 12,
        FONT_TINY,
        GRAY
    )

    draw_text(
        "WASD / ARROWS",
        30,
        y + 34,
        FONT_SMALL,
        WHITE
    )

    draw_text(
        "AI ANALYSIS",
        190,
        y + 12,
        FONT_TINY,
        GRAY
    )

    draw_text(
        "BFS / DFS / A* in menu",
        190,
        y + 34,
        FONT_SMALL,
        WHITE
    )

    draw_text(
        "C",
        430,
        y + 12,
        FONT_TINY,
        GRAY
    )

    draw_text(
        "Security Puzzle",
        430,
        y + 34,
        FONT_SMALL,
        WHITE
    )

    draw_text(
        "R",
        620,
        y + 12,
        FONT_TINY,
        GRAY
    )

    draw_text(
        "Restart",
        620,
        y + 34,
        FONT_SMALL,
        WHITE
    )

    draw_text(
        "SCORE",
        850,
        y + 12,
        FONT_TINY,
        GRAY
    )

    draw_text(
        "+100 KEY  +200 CSP  +300 TREASURE",
        850,
        y + 34,
        FONT_TINY,
        WHITE
    )

    draw_text(
        "ESC",
        740,
        y + 12,
        FONT_TINY,
        GRAY
    )

    draw_text(
        "Menu",
        740,
        y + 34,
        FONT_SMALL,
        WHITE
    )


# ============================================================
# CSP SCREEN
# ============================================================

def draw_csp_overlay():

    overlay = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (5, 8, 15, 225)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    width = min(
        760,
        SCREEN_WIDTH - 60
    )

    height = min(
        610,
        SCREEN_HEIGHT - 60
    )

    x = (
        SCREEN_WIDTH - width
    ) // 2

    y = (
        SCREEN_HEIGHT - height
    ) // 2

    pygame.draw.rect(
        screen,
        PANEL,
        (x, y, width, height),
        border_radius=18
    )

    pygame.draw.rect(
        screen,
        CYAN,
        (x, y, width, height),
        2,
        border_radius=18
    )

    draw_centered_text(
        "SECURITY TERMINAL",
        SCREEN_WIDTH // 2,
        y + 25,
        FONT_TITLE,
        CYAN
    )

    draw_centered_text(
        "Constraint Satisfaction Puzzle",
        SCREEN_WIDTH // 2,
        y + 75,
        FONT_SMALL,
        GRAY
    )

    draw_centered_text(
        "Assign numbers 1–4 to A, B, C and D.",
        SCREEN_WIDTH // 2,
        y + 115,
        FONT_NORMAL,
        WHITE
    )

    draw_centered_text(
        "Each number may be used only once.",
        SCREEN_WIDTH // 2,
        y + 145,
        FONT_SMALL,
        GRAY
    )

    # Constraints box
    constraint_rect = pygame.Rect(
        x + 35,
        y + 180,
        width - 70,
        100
    )

    pygame.draw.rect(
        screen,
        BG,
        constraint_rect,
        border_radius=10
    )

    draw_text(
        "CONSTRAINTS",
        x + 55,
        y + 195,
        FONT_SMALL,
        YELLOW
    )

    constraints = [
        "A < B",
        "C > A",
        "D > C",
        "B ≠ C"
    ]

    cx = x + 55

    for constraint in constraints:

        draw_text(
            constraint,
            cx,
            y + 230,
            FONT_SMALL,
            WHITE
        )

        cx += 150

    # Input fields
    variables = ["A", "B", "C", "D"]

    field_y = y + 310

    field_width = 110

    spacing = 35

    total_width = (
        4 * field_width
        + 3 * spacing
    )

    start_x = (
        SCREEN_WIDTH - total_width
    ) // 2

    for i, variable in enumerate(variables):

        field_x = (
            start_x
            + i * (field_width + spacing)
        )

        selected = (
            variable == csp_selected
        )

        draw_centered_text(
            variable,
            field_x + field_width // 2,
            field_y,
            FONT_MEDIUM,
            CYAN if selected else WHITE
        )

        color = CYAN if selected else PANEL_LIGHT

        pygame.draw.rect(
            screen,
            color,
            (
                field_x,
                field_y + 40,
                field_width,
                55
            ),
            border_radius=8
        )

        value = csp_values[variable]

        draw_centered_text(
            value if value else "?",
            field_x + field_width // 2,
            field_y + 53,
            FONT_BIG,
            BG if selected else WHITE
        )

    # Message
    message_color = (
        GREEN
        if csp_message_good
        else RED
        if csp_message.startswith("✗")
        else WHITE
    )

    draw_centered_text(
        csp_message,
        SCREEN_WIDTH // 2,
        y + 425,
        FONT_SMALL,
        message_color
    )

    # Buttons
    submit_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - 170,
        y + 465,
        340,
        45
    )

    pygame.draw.rect(
        screen,
        GREEN,
        submit_rect,
        border_radius=10
    )

    draw_centered_text(
        "ENTER  •  SUBMIT SOLUTION",
        SCREEN_WIDTH // 2,
        y + 477,
        FONT_SMALL,
        BG
    )

    # AI solution information
    if show_csp_ai_solution:

        draw_centered_text(
            f"AI BACKTRACKING: {csp_attempts} attempts",
            SCREEN_WIDTH // 2,
            y + 525,
            FONT_TINY,
            CYAN
        )

        draw_centered_text(
            "AI Solution: A=1  B=2  C=3  D=4",
            SCREEN_WIDTH // 2,
            y + 545,
            FONT_TINY,
            GREEN
        )

    else:

        draw_centered_text(
            "Press ESC to leave the terminal",
            SCREEN_WIDTH // 2,
            y + 535,
            FONT_TINY,
            GRAY
        )


# ============================================================
# MENU
# ============================================================

def get_menu_buttons():
    """Return the rectangles used by the main-menu buttons."""
    button_width = 360
    button_height = 55
    start_y = 285
    gap = 14

    labels = [
        "START MISSION",
        "HOW TO PLAY",
        "AI ANALYSIS",
        "EXIT"
    ]

    buttons = []

    for i, label in enumerate(labels):
        rect = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2,
            start_y + i * (button_height + gap),
            button_width,
            button_height
        )
        buttons.append((label, rect))

    return buttons


def update_menu_hover():
    """Select the menu item currently under the mouse cursor."""
    global menu_selected

    mouse_pos = pygame.mouse.get_pos()

    for i, (_, rect) in enumerate(get_menu_buttons()):
        if rect.collidepoint(mouse_pos):
            menu_selected = i
            return


def draw_menu():

    screen.fill(BG)

    draw_centered_text(
        "COGNITIVE QUEST",
        SCREEN_WIDTH // 2,
        130,
        FONT_TITLE,
        CYAN
    )

    draw_centered_text(
        "An AI-Driven Adaptive Strategy Game",
        SCREEN_WIDTH // 2,
        185,
        FONT_NORMAL,
        GRAY
    )

    draw_centered_text(
        "SEARCH  •  CSP  •  KNOWLEDGE  •  MINIMAX",
        SCREEN_WIDTH // 2,
        225,
        FONT_SMALL,
        PURPLE
    )

    mouse_pos = pygame.mouse.get_pos()

    for i, (label, rect) in enumerate(get_menu_buttons()):

        hovered = rect.collidepoint(mouse_pos)
        selected = (i == menu_selected)

        # Hovering the button also updates keyboard selection.
        if hovered:
            menu_color = CYAN
            text_color = BG
            border_color = CYAN
        elif selected:
            menu_color = PANEL_LIGHT
            text_color = WHITE
            border_color = CYAN
        else:
            menu_color = PANEL
            text_color = WHITE
            border_color = PANEL_LIGHT

        pygame.draw.rect(
            screen,
            menu_color,
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            border_color,
            rect,
            2,
            border_radius=12
        )

        button_text = (
            "▶  " + label
            if selected or hovered
            else label
        )

        draw_centered_text(
            button_text,
            rect.centerx,
            rect.y + 17,
            FONT_MEDIUM,
            text_color
        )

    draw_centered_text(
        "Move the mouse and CLICK an option",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT - 105,
        FONT_SMALL,
        WHITE
    )

    draw_centered_text(
        "Keyboard: ↑ ↓ to select  •  ENTER to confirm",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT - 75,
        FONT_TINY,
        GRAY
    )


# ============================================================
# AI ANALYSIS SCREEN
# ============================================================

def get_analysis_buttons():

    _, _, _, panel_x = get_layout()

    button_width = 260
    button_height = 48
    start_y = 185
    gap = 12

    labels = ["BFS", "DFS", "A*"]

    buttons = []

    for i, label in enumerate(labels):

        rect = pygame.Rect(
            panel_x + 15,
            start_y + i * (button_height + gap),
            button_width,
            button_height
        )

        buttons.append((label, rect))

    return buttons


def run_analysis_algorithm(index):

    global analysis_selected

    analysis_selected = index

    if index == 0:
        run_bfs()
    elif index == 1:
        run_dfs()
    elif index == 2:
        run_astar()


def update_analysis_hover():

    global analysis_selected

    mouse_pos = pygame.mouse.get_pos()

    for i, (_, rect) in enumerate(get_analysis_buttons()):
        if rect.collidepoint(mouse_pos):
            analysis_selected = i
            return


def handle_analysis_click(pos):

    for i, (_, rect) in enumerate(get_analysis_buttons()):

        if rect.collidepoint(pos):
            run_analysis_algorithm(i)
            return

    back_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - 130,
        SCREEN_HEIGHT - 72,
        260,
        42
    )

    if back_rect.collidepoint(pos):
        global game_state
        game_state = "MENU"


def draw_ai_analysis():

    screen.fill(BG)

    draw_centered_text(
        "AI ANALYSIS",
        SCREEN_WIDTH // 2,
        55,
        FONT_TITLE,
        CYAN
    )

    draw_centered_text(
        "Compare BFS, DFS and A* on the same game map",
        SCREEN_WIDTH // 2,
        95,
        FONT_SMALL,
        GRAY
    )

    # Show the selected algorithm's result on the map.
    draw_map()

    _, _, _, panel_x = get_layout()

    panel_rect = pygame.Rect(
        panel_x,
        125,
        290,
        SCREEN_HEIGHT - 220
    )

    pygame.draw.rect(
        screen,
        PANEL,
        panel_rect,
        border_radius=14
    )

    pygame.draw.rect(
        screen,
        PANEL_LIGHT,
        panel_rect,
        1,
        border_radius=14
    )

    draw_text(
        "SEARCH ALGORITHMS",
        panel_x + 15,
        145,
        FONT_MEDIUM,
        WHITE
    )

    mouse_pos = pygame.mouse.get_pos()

    for i, (label, rect) in enumerate(get_analysis_buttons()):

        hovered = rect.collidepoint(mouse_pos)
        selected = i == analysis_selected

        if hovered:
            fill = CYAN
            text_color = BG
            border = CYAN
        elif selected:
            fill = PANEL_LIGHT
            text_color = WHITE
            border = CYAN
        else:
            fill = PANEL_LIGHT
            text_color = WHITE
            border = GRAY

        pygame.draw.rect(
            screen,
            fill,
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            border,
            rect,
            2,
            border_radius=10
        )

        draw_centered_text(
            label,
            rect.centerx,
            rect.y + 12,
            FONT_MEDIUM,
            text_color
        )

    # --------------------------------------------------------
    # Algorithm information
    # --------------------------------------------------------

    descriptions = {
        "BFS": {
            "title": "Breadth-First Search",
            "lines": [
                "Explores the grid level by level.",
                "Finds a shortest path when all moves",
                "have the same cost."
            ],
            "why": "Useful for shortest-path problems",
            "key": "B"
        },
        "DFS": {
            "title": "Depth-First Search",
            "lines": [
                "Explores deeply along one branch",
                "before backtracking to another branch."
            ],
            "why": "Useful for exploration and traversal",
            "key": "F"
        },
        "A*": {
            "title": "A* Search",
            "lines": [
                "Combines path cost with a heuristic",
                "to guide the search toward the goal."
            ],
            "why": "Efficient pathfinding for game AI",
            "key": "P"
        }
    }

    name = current_search_name

    if name == "None":

        draw_text(
            "RESULT",
            panel_x + 15,
            390,
            FONT_SMALL,
            PURPLE
        )

        draw_text(
            "Select an algorithm above.",
            panel_x + 15,
            420,
            FONT_NORMAL,
            GRAY
        )

        draw_text(
            "The search result will appear",
            panel_x + 15,
            448,
            FONT_SMALL,
            GRAY
        )

        draw_text(
            "on the map and here.",
            panel_x + 15,
            470,
            FONT_SMALL,
            GRAY
        )

    else:

        info = descriptions[name]

        draw_text(
            "ALGORITHM",
            panel_x + 15,
            385,
            FONT_SMALL,
            PURPLE
        )

        draw_text(
            info["title"],
            panel_x + 15,
            408,
            FONT_NORMAL,
            CYAN
        )

        draw_text(
            "RESULT",
            panel_x + 15,
            442,
            FONT_SMALL,
            PURPLE
        )

        draw_text(
            f"Explored cells: {len(current_search_explored)}",
            panel_x + 15,
            466,
            FONT_SMALL,
            YELLOW
        )

        draw_text(
            f"Path length: {len(current_search_path)}",
            panel_x + 15,
            490,
            FONT_SMALL,
            GREEN
        )

        draw_text(
            "WHY IT MATTERS",
            panel_x + 15,
            524,
            FONT_SMALL,
            PURPLE
        )

        y = 548
        for line in info["lines"]:
            draw_text(
                line,
                panel_x + 15,
                y,
                FONT_TINY,
                WHITE
            )
            y += 19

        draw_text(
            info["why"],
            panel_x + 15,
            y + 5,
            FONT_TINY,
            GRAY
        )

    # --------------------------------------------------------
    # Enemy AI explanation
    # --------------------------------------------------------

    draw_text(
        "ENEMY GAMEPLAY AI",
        panel_x + 15,
        635,
        FONT_SMALL,
        PURPLE
    )

    draw_text(
        "A* + Minimax runs automatically",
        panel_x + 15,
        658,
        FONT_TINY,
        WHITE
    )

    draw_text(
        "A* finds a route; Minimax chooses",
        panel_x + 15,
        678,
        FONT_TINY,
        GRAY
    )

    draw_text(
        "the enemy's movement decision.",
        panel_x + 15,
        696,
        FONT_TINY,
        GRAY
    )

    back_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - 130,
        SCREEN_HEIGHT - 72,
        260,
        42
    )

    pygame.draw.rect(
        screen,
        PANEL_LIGHT,
        back_rect,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        CYAN,
        back_rect,
        2,
        border_radius=10
    )

    draw_centered_text(
        "BACK TO MENU",
        back_rect.centerx,
        back_rect.y + 10,
        FONT_SMALL,
        WHITE
    )

    draw_centered_text(
        "Click an algorithm  •  ESC to return",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT - 25,
        FONT_TINY,
        GRAY
    )


# ============================================================
# HOW TO PLAY
# ============================================================

def draw_how_to_play():

    screen.fill(BG)

    draw_centered_text(
        "HOW TO PLAY",
        SCREEN_WIDTH // 2,
        70,
        FONT_TITLE,
        CYAN
    )

    instructions = [

        ("1", "Explore the map"),
        ("2", "Find the security key"),
        ("3", "Reach the locked security door"),
        ("4", "Solve the CSP security puzzle"),
        ("5", "Collect the treasure"),
        ("6", "Avoid the AI enemy"),
        ("7", "Reach the goal")
    ]

    y = 150

    for number, text in instructions:

        draw_text(
            number,
            SCREEN_WIDTH // 2 - 280,
            y,
            FONT_MEDIUM,
            YELLOW
        )

        draw_text(
            text,
            SCREEN_WIDTH // 2 - 230,
            y,
            FONT_NORMAL,
            WHITE
        )

        y += 50

    draw_text(
        "AI SYSTEMS",
        SCREEN_WIDTH // 2 - 280,
        y + 20,
        FONT_MEDIUM,
        PURPLE
    )

    systems = [
        "BFS / DFS / A* - Search and pathfinding",
        "CSP / Backtracking - Security puzzle",
        "Minimax - Enemy decision making",
        "Knowledge Base - Game-state reasoning",
        "Adaptive AI - Dynamic difficulty"
    ]

    y += 65

    for system in systems:

        draw_text(
            "•",
            SCREEN_WIDTH // 2 - 280,
            y,
            FONT_NORMAL,
            CYAN
        )

        draw_text(
            system,
            SCREEN_WIDTH // 2 - 255,
            y,
            FONT_SMALL,
            WHITE
        )

        y += 32

    draw_centered_text(
        "Press ESC to return",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT - 60,
        FONT_SMALL,
        GRAY
    )


# ============================================================
# LEVEL COMPLETE
# ============================================================

def draw_level_complete():

    overlay = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (5, 10, 15, 210)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    draw_centered_text(
        "LEVEL COMPLETE",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT // 2 - 100,
        FONT_TITLE,
        GREEN
    )

    draw_centered_text(
        f"Moves: {move_count}",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT // 2 - 40,
        FONT_NORMAL,
        WHITE
    )

    if current_level < len(LEVELS) - 1:

        draw_centered_text(
            "Press ENTER for the next level",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 40,
            FONT_MEDIUM,
            CYAN
        )

    else:

        draw_centered_text(
            "Final level completed!",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 20,
            FONT_MEDIUM,
            CYAN
        )

        draw_centered_text(
            "Press ENTER to finish the mission",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 70,
            FONT_SMALL,
            WHITE
        )


# ============================================================
# MISSION COMPLETE
# ============================================================

def draw_mission_complete():

    screen.fill(BG)

    draw_centered_text(
        "MISSION COMPLETE",
        SCREEN_WIDTH // 2,
        180,
        FONT_TITLE,
        GREEN
    )

    draw_centered_text(
        "You escaped the AI-controlled fortress.",
        SCREEN_WIDTH // 2,
        250,
        FONT_NORMAL,
        WHITE
    )

    draw_centered_text(
        f"FINAL SCORE: {score}",
        SCREEN_WIDTH // 2,
        330,
        FONT_BIG,
        YELLOW
    )

    draw_centered_text(
        "SEARCH  •  CSP  •  MINIMAX  •  KNOWLEDGE",
        SCREEN_WIDTH // 2,
        400,
        FONT_SMALL,
        CYAN
    )

    draw_centered_text(
        "Press ENTER to return to the main menu",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT - 100,
        FONT_SMALL,
        GRAY
    )


# ============================================================
# GAME OVER
# ============================================================

def draw_game_over():

    overlay = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (10, 5, 10, 220)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    draw_centered_text(
        "MISSION FAILED",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT // 2 - 80,
        FONT_TITLE,
        RED
    )

    draw_centered_text(
        "The AI enemy caught you.",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT // 2 - 20,
        FONT_NORMAL,
        WHITE
    )

    draw_centered_text(
        f"Final Score: {score}",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT // 2 + 20,
        FONT_MEDIUM,
        YELLOW
    )

    draw_centered_text(
        "Press R to restart",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT // 2 + 50,
        FONT_MEDIUM,
        CYAN
    )

    draw_centered_text(
        "Press ESC for menu",
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT // 2 + 100,
        FONT_SMALL,
        GRAY
    )


# ============================================================
# PLAYING SCREEN
# ============================================================

def draw_game():

    screen.fill(BG)

    draw_hud()

    draw_map()

    _, _, _, panel_x = get_layout()

    draw_objectives(panel_x)

    draw_ai_panel(panel_x)

    draw_event_panel(panel_x)

    draw_bottom_bar()

    if csp_puzzle_active:
        draw_csp_overlay()

    elif level_complete:
        draw_level_complete()

    elif game_over:
        draw_game_over()


# ============================================================
# MENU MOUSE HANDLING
# ============================================================

def handle_menu_click(pos):

    global game_state
    global menu_selected
    global score

    for i, (_, rect) in enumerate(get_menu_buttons()):

        if rect.collidepoint(pos):

            menu_selected = i

            if i == 0:
                score = 0
                load_level(0)
                game_state = "PLAYING"

            elif i == 1:
                game_state = "HOW_TO_PLAY"

            elif i == 2:
                global current_search_name
                global current_search_path
                global current_search_explored
                current_search_name = "None"
                current_search_path = []
                current_search_explored = []
                game_state = "AI_ANALYSIS"

            elif i == 3:
                pygame.quit()
                sys.exit()

            return


# ============================================================
# KEYBOARD HANDLING
# ============================================================

def handle_csp_key(event):

    global csp_selected

    variables = ["A", "B", "C", "D"]

    if event.key == pygame.K_ESCAPE:

        global csp_puzzle_active

        csp_puzzle_active = False

        return

    if event.key == pygame.K_LEFT:

        index = variables.index(csp_selected)

        index = (index - 1) % 4

        csp_selected = variables[index]

        return

    if event.key == pygame.K_RIGHT:

        index = variables.index(csp_selected)

        index = (index + 1) % 4

        csp_selected = variables[index]

        return

    if event.key == pygame.K_TAB:

        index = variables.index(csp_selected)

        index = (index + 1) % 4

        csp_selected = variables[index]

        return

    if event.key in [
        pygame.K_1,
        pygame.K_2,
        pygame.K_3,
        pygame.K_4
    ]:

        value = {
            pygame.K_1: "1",
            pygame.K_2: "2",
            pygame.K_3: "3",
            pygame.K_4: "4"
        }[event.key]

        csp_values[csp_selected] = value

        index = variables.index(csp_selected)

        if index < 3:

            csp_selected = variables[index + 1]

        return

    if event.key == pygame.K_BACKSPACE:

        csp_values[csp_selected] = ""

        return

    if event.key == pygame.K_RETURN:

        solve_player_csp()

        return


def handle_playing_key(event):

    global game_state
    global score

    if csp_puzzle_active:

        handle_csp_key(event)

        return

    if level_complete:

        if event.key == pygame.K_RETURN:

            advance_level()

        return

    if game_over:

        if event.key == pygame.K_r:

            load_level(current_level)

            game_state = "PLAYING"

        elif event.key == pygame.K_ESCAPE:

            game_state = "MENU"

        return

    if event.key == pygame.K_ESCAPE:

        game_state = "MENU"

        return

    if event.key == pygame.K_r:

        load_level(current_level)

        return

    # Movement
    if event.key in [pygame.K_UP, pygame.K_w]:

        move_player(-1, 0)

    elif event.key in [pygame.K_DOWN, pygame.K_s]:

        move_player(1, 0)

    elif event.key in [pygame.K_LEFT, pygame.K_a]:

        move_player(0, -1)

    elif event.key in [pygame.K_RIGHT, pygame.K_d]:

        move_player(0, 1)

    # CSP
    elif event.key == pygame.K_c:

        if key_collected:

            open_csp_puzzle()

        else:

            global message

            message = (
                "Find the security key before opening the terminal."
            )


# ============================================================
# MAIN LOOP
# ============================================================

load_level(0)

# Start with START MISSION selected.
menu_selected = 0

running = True

while running:

    clock.tick(60)

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.MOUSEMOTION:

            # Live hover feedback on the main menu and AI Analysis.
            if game_state == "MENU":
                update_menu_hover()
            elif game_state == "AI_ANALYSIS":
                update_analysis_hover()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1 and game_state == "MENU":
                handle_menu_click(event.pos)
            elif event.button == 1 and game_state == "AI_ANALYSIS":
                handle_analysis_click(event.pos)

        elif event.type == pygame.KEYDOWN:

            if game_state == "MENU":

                if event.key == pygame.K_ESCAPE:

                    running = False

                elif event.key == pygame.K_UP:

                    menu_selected = (
                        menu_selected - 1
                    ) % len(get_menu_buttons())

                elif event.key == pygame.K_DOWN:

                    menu_selected = (
                        menu_selected + 1
                    ) % len(get_menu_buttons())

                elif event.key == pygame.K_RETURN:

                    # Activate the currently selected menu item.
                    label, rect = get_menu_buttons()[menu_selected]
                    handle_menu_click(rect.center)

            elif game_state == "HOW_TO_PLAY":

                if event.key == pygame.K_ESCAPE:

                    game_state = "MENU"

            elif game_state == "AI_ANALYSIS":

                if event.key == pygame.K_ESCAPE:

                    game_state = "MENU"

                elif event.key == pygame.K_LEFT:

                    analysis_selected = (analysis_selected - 1) % 3
                    run_analysis_algorithm(analysis_selected)

                elif event.key == pygame.K_RIGHT:

                    analysis_selected = (analysis_selected + 1) % 3
                    run_analysis_algorithm(analysis_selected)

                elif event.key == pygame.K_RETURN:

                    run_analysis_algorithm(analysis_selected)

                elif event.key == pygame.K_b:

                    run_analysis_algorithm(0)

                elif event.key == pygame.K_f:

                    run_analysis_algorithm(1)

                elif event.key == pygame.K_p:

                    run_analysis_algorithm(2)

            elif game_state == "PLAYING":

                handle_playing_key(event)

            elif game_state == "MISSION_COMPLETE":

                if event.key == pygame.K_RETURN:

                    game_state = "MENU"

            elif game_state == "GAME_OVER":

                if event.key == pygame.K_r:

                    load_level(current_level)
                    game_state = "PLAYING"

                elif event.key == pygame.K_ESCAPE:

                    game_state = "MENU"

    # --------------------------------------------------------
    # GAME UPDATE
    # --------------------------------------------------------

    if game_state == "PLAYING":

        if not csp_puzzle_active and not game_over:

            update_enemy()

            update_knowledge()

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    if game_state == "MENU":

        draw_menu()

    elif game_state == "HOW_TO_PLAY":

        draw_how_to_play()

    elif game_state == "AI_ANALYSIS":

        draw_ai_analysis()

    elif game_state == "PLAYING":

        draw_game()

    elif game_state == "MISSION_COMPLETE":

        draw_mission_complete()

    elif game_state == "GAME_OVER":

        draw_game_over()

    pygame.display.flip()


pygame.quit()
sys.exit()