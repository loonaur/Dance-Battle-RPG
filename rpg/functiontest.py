import unittest
from unittest.mock import patch
from rpg.game import Game
import random


class TestGameFullRun(unittest.TestCase):
    """
    Unit test class to simulate a full game run using random inputs.
    It limits the number of actions performed in the game loop to
    avoid indefinite runs.
    """

    def random_gameplay_input(self, prompt: str, action_count: int,
                              max_actions: int) -> str:
        """
        Randomly returns a valid input choice for different game situations,
        and stops after a defined number of actions.

        Args:
            prompt (str): The game's prompt for the player's next action.
            action_count (int): The number of actions taken so far.
            max_actions (int): The maximum number of actions allowed.

        Returns:
            str: A randomly chosen input representing the player's action.
        """
        if action_count >= max_actions:
            return "5"

        if "What do you want to do?" in prompt:
            return random.choice(["0", "1", "2", "5"])
        elif "Which one do you want to go through?" in prompt:
            return random.choice(["0", "1"])
        elif "Do you want to" in prompt:
            return random.choice(["0", "1"])
        else:
            return "0"

    @patch("builtins.input")
    def test_game_full_run(self, mock_input: unittest.mock.Mock) -> None:
        """
        This test simulates a full game run with random inputs, limited to
        a certain number of actions.

        Args:
            mock_input (unittest.mock.Mock): Mock object to simulate input.
        """
        game = Game()
        max_actions = 50
        action_count = 0

        def side_effect(prompt: str) -> str:
            nonlocal action_count
            response = self.random_gameplay_input(
                prompt, action_count, max_actions
            )
            action_count += 1
            return response

        mock_input.side_effect = side_effect

        try:
            game.play()
        except SystemExit:
            pass

        print(f"Game simulation completed after {action_count} actions.")


if __name__ == "__main__":
    unittest.main()
