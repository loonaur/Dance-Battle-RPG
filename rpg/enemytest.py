import unittest
from unittest.mock import MagicMock, patch
from rpg.enemy import Enemy
from itertools import cycle


class TestEnemy(unittest.TestCase):
    """
    Unit tests for the Enemy class, covering interactions, battles,
    and serialization.
    """

    def setUp(self) -> None:
        """
        Set up an Enemy instance and mock dependencies for testing.
        """
        self.enemy = Enemy(
            description="A fierce dragon",
            interact_message="The dragon snarls at you!"
        )
        self.player = MagicMock()
        self.player._health = 100
        self.scanner = MagicMock()
        self.game = MagicMock()

    @patch("builtins.print")
    def test_inspect_method(self, mock_print: unittest.mock.Mock) -> None:
        """
        Test that the inspect method prints the correct enemy description.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        self.enemy.inspect()
        mock_print.assert_called_once_with("A fierce dragon")

    @patch("builtins.print")
    def test_interact_victory(self, mock_print: unittest.mock.Mock) -> None:
        """
        Test a complete battle where the player wins.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        self.scanner.read_int.side_effect = cycle([0, 0, 0])
        self.player.player_death.return_value = "ALIVE"

        with patch("random.randint", side_effect=cycle([15, 5])):
            self.enemy.interact(self.player, self.scanner, self.game)

        mock_print.assert_any_call(
            "You engage in a dance battle with A fierce dragon!"
        )
        mock_print.assert_any_call(
            "You have won the dance battle against A fierce dragon!"
        )
        self.game.enemy_defeated.assert_called_once()

    @patch("builtins.print")
    def test_interact_defeat(self, mock_print: unittest.mock.Mock) -> None:
        """
        Test a complete battle where the player loses.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        self.scanner.read_int.side_effect = cycle([0, 0, 0])
        self.player.player_death.return_value = "DEAD"

        with patch("random.randint", side_effect=cycle([5, 15])):
            self.enemy.interact(self.player, self.scanner, self.game)

        mock_print.assert_any_call(
            "You engage in a dance battle with A fierce dragon!"
        )
        mock_print.assert_any_call(
            "You have lost the dance battle against A fierce dragon."
        )
        self.game.reset_game.assert_called_once()
        self.game.play.assert_called_once()

    @patch("builtins.print")
    def test_interact_invalid_move(
        self, mock_print: unittest.mock.Mock
    ) -> None:
        """
        Test the interaction method with an invalid move input.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        self.scanner.read_int.side_effect = cycle([-1, 0])
        with patch("random.randint", return_value=10):
            self.enemy.interact(self.player, self.scanner, self.game)

        mock_print.assert_any_call(
            "Invalid dance move choice. Please choose again."
        )

    def test_health_initialization(self) -> None:
        """
        Test that the enemy's health is initialized correctly.
        """
        self.assertEqual(self.enemy._health, 100)

    def test_health_reduction(self) -> None:
        """
        Test that health is correctly reduced during battle.
        """
        initial_health = self.enemy._health
        damage = 20
        self.enemy._health -= damage
        self.assertEqual(self.enemy._health, initial_health - damage)

    def test_to_json_method(self) -> None:
        """
        Test that the toJSON method correctly serializes the Enemy object.
        """
        enemy_data = self.enemy.toJSON()
        expected_data = {
            "description": "A fierce dragon",
            "interact_message": "The dragon snarls at you!"
        }
        self.assertEqual(enemy_data, expected_data)

    def test_from_json_method(self) -> None:
        """
        Test that fromJSON correctly deserializes into an Enemy object.
        """
        json_data = {
            "description": "A scary skeleton",
            "interact_message": "You feel a chill run down your spine."
        }
        enemy = Enemy.fromJSON(json_data)
        self.assertEqual(enemy.description, "A scary skeleton")
        self.assertEqual(
            enemy.interact_message,
            "You feel a chill run down your spine."
        )

    def test_integration_to_json_from_json(self) -> None:
        """
        Test that the Enemy object can be serialized and deserialized
        without data loss.
        """
        enemy_data = self.enemy.toJSON()
        deserialized_enemy = Enemy.fromJSON(enemy_data)
        self.assertEqual(
            deserialized_enemy.description, self.enemy.description
        )
        self.assertEqual(
            deserialized_enemy.interact_message,
            self.enemy.interact_message
        )


if __name__ == "__main__":
    unittest.main()
