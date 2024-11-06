import unittest
from unittest.mock import MagicMock, patch
from rpg.healer import Healer


class TestHealer(unittest.TestCase):
    """
    Unit tests for the Healer class to ensure its correct behavior,
    including player interactions and initialization.
    """

    def setUp(self) -> None:
        """
        Set up a Healer instance and mock dependencies for testing.
        """
        self.healer = Healer(
            description="A kind and wise healer",
            interact_message=(
                "The healer chants softly and restores your health."
            )
        )
        self.player = MagicMock()
        self.player._health = 50

    @patch("builtins.print")
    def test_inspect_method(self, mock_print: unittest.mock.Mock) -> None:
        """
        Test that the inspect method prints the correct healer description.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        self.healer.inspect()
        mock_print.assert_called_once_with("A kind and wise healer")

    @patch("builtins.print")
    def test_interact_method(self, mock_print: unittest.mock.Mock) -> None:
        """
        Test that the healer interacts correctly and restores player health.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        self.healer.interact(self.player)
        self.assertEqual(self.player._health, 100)
        mock_print.assert_called_once_with(
            "A kind and wise healer heals you, restoring your full health!"
        )

    def test_initialization(self) -> None:
        """
        Test that the healer initializes correctly with the given
        description and interact message.
        """
        healer = Healer(
            description="A gentle healer with magical powers",
            interact_message="The healer blesses you with a warm light."
        )
        self.assertEqual(
            healer.description,
            "A gentle healer with magical powers"
        )
        self.assertEqual(
            healer.interact_message,
            "The healer blesses you with a warm light."
        )


if __name__ == "__main__":
    unittest.main()
