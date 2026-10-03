# ============================================================
# COGNITIVE QUEST
# ADAPTIVE DIFFICULTY AI
# ============================================================

class AdaptiveDifficulty:

    def __init__(self):
        self.level = 1
        self.status = "Easy"
        self.minimax_depth = 2
        self.enemy_delay = 0.8

    def calculate_difficulty(
        self,
        player_health,
        move_count,
        treasure_collected,
        enemy_distance
    ):
        score = 0

        # Player has low health
        if player_health <= 50:
            score += 2

        # Player has made many moves
        if move_count >= 15:
            score += 1

        if move_count >= 30:
            score += 1

        # Treasure has already been collected
        if treasure_collected:
            score += 2

        # Enemy is close
        if enemy_distance <= 3:
            score += 1

        if enemy_distance <= 1:
            score += 2

        # ----------------------------------------------------
        # Difficulty levels
        # ----------------------------------------------------

        if score <= 2:
            self.level = 1
            self.status = "Easy"
            self.minimax_depth = 2
            self.enemy_delay = 0.9

        elif score <= 5:
            self.level = 2
            self.status = "Medium"
            self.minimax_depth = 3
            self.enemy_delay = 0.7

        else:
            self.level = 3
            self.status = "Hard"
            self.minimax_depth = 4
            self.enemy_delay = 0.5

        return self.level

    def get_minimax_depth(self):
        return self.minimax_depth

    def get_enemy_delay(self):
        return self.enemy_delay

    def get_status(self):
        return self.status

    def get_level(self):
        return self.level


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    ai = AdaptiveDifficulty()

    print("Adaptive Difficulty Test")
    print("-------------------------")

    ai.calculate_difficulty(
        player_health=100,
        move_count=5,
        treasure_collected=False,
        enemy_distance=6
    )

    print("Status:", ai.get_status())
    print("Level:", ai.get_level())
    print("Minimax Depth:", ai.get_minimax_depth())
    print("Enemy Delay:", ai.get_enemy_delay())

    print()

    ai.calculate_difficulty(
        player_health=40,
        move_count=20,
        treasure_collected=True,
        enemy_distance=2
    )

    print("After difficulty increase:")
    print("Status:", ai.get_status())
    print("Level:", ai.get_level())
    print("Minimax Depth:", ai.get_minimax_depth())
    print("Enemy Delay:", ai.get_enemy_delay())