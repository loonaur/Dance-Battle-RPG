import unittest
from unittest.mock import patch
from rpg.npc import NPC


class TestNPC(unittest.TestCase):
    """
    Unit tests for the NPC class, including initialization, interactions,
    and JSON serialization.
    """

    def setUp(self) -> None:
        """Set up an NPC instance for use in the tests."""
        self.npc = NPC(
            description="A friendly merchant",
            interact_message="Hello there! Would you like to trade?"
        )

    def test_initialization(self) -> None:
        """Test the initialization of the NPC object."""
        npc = NPC(
            description="A wise old sage",
            interact_message="The secrets of the universe are hidden."
        )
        self.assertEqual(npc.description, "A wise old sage")
        self.assertEqual(
            npc.interact_message,
            "The secrets of the universe are hidden."
        )

    @patch("builtins.print")
    def test_inspect_method(self, mock_print: unittest.mock.Mock) -> None:
        """
        Test that the inspect method prints the correct NPC description.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        self.npc.inspect()
        mock_print.assert_called_once_with("A friendly merchant")

    @patch("builtins.print")
    def test_interact_method(self, mock_print: unittest.mock.Mock) -> None:
        """
        Test that the interact method prints the correct interaction message.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        player_mock = unittest.mock.MagicMock()
        self.npc.interact(player_mock)
        mock_print.assert_called_once_with(
            "Hello there! Would you like to trade?"
        )

    def test_to_json_method(self) -> None:
        """
        Test that the toJSON method correctly serializes the NPC object.
        """
        npc_data = self.npc.toJSON()
        expected_data = {
            "description": "A friendly merchant",
            "interact_message": "Hello there! Would you like to trade?"
        }
        self.assertEqual(npc_data, expected_data)

    def test_from_json_method(self) -> None:
        """
        Test that fromJSON correctly deserializes into an NPC object.
        """
        json_data = {
            "description": "A mischievous goblin",
            "interact_message": "Hehehe, what do you want, human?"
        }
        npc = NPC.fromJSON(json_data)
        self.assertEqual(npc.description, "A mischievous goblin")
        self.assertEqual(
            npc.interact_message,
            "Hehehe, what do you want, human?"
        )

    def test_to_json_and_from_json_integration(self) -> None:
        """
        Test that an NPC object can be serialized and deserialized without
        data loss.
        """
        npc_data = self.npc.toJSON()
        deserialized_npc = NPC.fromJSON(npc_data)
        self.assertEqual(
            deserialized_npc.description,
            self.npc.description
        )
        self.assertEqual(
            deserialized_npc.interact_message,
            self.npc.interact_message
        )


if __name__ == "__main__":
    unittest.main()
