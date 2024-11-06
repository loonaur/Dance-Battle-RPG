import unittest
from unittest.mock import patch
from rpg.game import Game


class TestMainGameLoop(unittest.TestCase):
    """
    Unit tests for the main game loop in the Game class.
    This test ensures that the game loop correctly processes user inputs
    and updates the game state.
    """

    @patch("builtins.input")
    def test_main_game_loop(self, mock_input: unittest.mock.Mock) -> None:
        """
        Integration test for the main game loop.
        Simulates user inputs and checks if the game state is updated
        as expected during a series of interactions.

        Args:
            mock_input (unittest.mock.Mock): Mock for simulating user input.
        """
        game = Game()

        inputs = [
            "0",
            "1",
            "0",
            "2",
            "0",
            "5"
        ]

        mock_input.side_effect = inputs

        try:
            game.play()
        except SystemExit:
            pass

        self.assertIsNotNone(game.player, "Player should be initialized.")
        self.assertGreaterEqual(len(game.rooms), 1,
                                "There should be rooms initialized.")
        self.assertEqual(game.enemies_defeated, 0,
                         "No enemies were encountered or defeated.")

        print("Main game loop test completed.")


if __name__ == "__main__":
    unittest.main()
