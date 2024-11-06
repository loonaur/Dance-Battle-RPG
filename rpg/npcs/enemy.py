from pydantic import Field, PrivateAttr
from rpg.npcs.npc import NPC
import random
from typing import Dict, Tuple, TypeVar

Player = TypeVar("Player")
Game = TypeVar("Game")
Scanner = TypeVar("Scanner")


class Enemy(NPC):
    """Represents an enemy NPC that
    the player can encounter in the game."""

    description: str = Field(..., description="Enemy description")
    _health: int = PrivateAttr(default=100)

    def inspect(self) -> None:
        """Displays the description of the enemy."""
        print(f"{self.description}")

    def interact(self, player: "Player", scanner: "Scanner",
                 game: "Game") -> None:

        """
        Handles the interaction between the player and the enemy.

        Initiates a dance battle with the player
        and manages the battle sequence.

        Args:
            player: The player object.
            scanner: The input scanner for reading player choices.
            game: The main game object to manage the game state.
        """
        print(f"You engage in a dance battle with {self.description}!")
        print(f"Your current health: {player._health}")

        player_moves: Dict[str, Tuple[int, int]] = {
            "Spin": (5, 15), "Flip": (10, 20),
            "Body roll": (15, 25)
        }
        enemy_moves: Dict[str, Tuple[int, int]] = {
            "Spin": (10, 20), "Flip": (15, 25),
            "Body roll": (15, 20)
        }

        while self._health > 0 and player._health > 0:
            print("\n--- Battle Status ---")
            print(f"Your health: {player._health} | "
                  f"{self.description}'s health: {self._health}")

            print("\nChoose your dance move:")
            for index, move in enumerate(player_moves.keys()):
                print(f"  ({index}) {move}")

            action_choice: int = scanner.read_int("> ")

            if 0 <= action_choice < len(player_moves):
                move_name: str = list(player_moves.keys())[action_choice]
                move_damage: int = random.randint(*player_moves[move_name])
                print(
                    f"You perform a {move_name}! "
                    f"It deals {move_damage} damage."
                )
                self._health -= move_damage

                if self._health <= 0:
                    print(
                        f"You have won the dance "
                        f"battle against {self.description}!"
                    )
                    game.enemy_defeated()
                    return

                enemy_move: str = random.choice(list(enemy_moves.keys()))
                enemy_damage: int = random.randint(*enemy_moves[enemy_move])
                print(f"{self.description} performs a {enemy_move}! "
                      f"It deals {enemy_damage} damage.")
                player._health -= enemy_damage

                if player._health <= 0:
                    print(
                        f"You have lost the dance "
                        f"battle against {self.description}."
                    )
                    if player.player_death() == "DEAD":
                        game.reset_game()
                        game.play()
                    break
            else:
                print("Invalid dance move choice. Please choose again.")
