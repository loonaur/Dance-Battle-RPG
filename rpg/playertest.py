import unittest
from unittest.mock import patch
from rpg.player import Player
from rpg.room import Room


class TestPlayer(unittest.TestCase):
    """
    Unit tests for the Player class, including initialization, room
    interactions, and room inspections.
    """

    def setUp(self) -> None:
        """Set up a real Room object for Player tests."""
        self.room = Room(
            description="A magical forest glade",
            doors=[],
            npcs=[]
        )
        self.player = Player(name="Hero")
        self.player.enter_room(self.room)

    def test_initialization(self) -> None:
        """
        Test Player initialization with name and default attributes.
        """
        player = Player(name="TestPlayer")
        self.assertEqual(player.name, "TestPlayer")
        self.assertEqual(player._health, 100)
        self.assertEqual(player._current_room, "")

    def test_enter_room(self) -> None:
        """
        Test the enter_room method changes the player's current room.
        """
        new_room = Room(
            description="A cozy library",
            doors=[],
            npcs=[]
        )
        self.player.enter_room(new_room)
        self.assertEqual(self.player._current_room, new_room)
        self.assertEqual(
            self.player._current_room.description,
            "A cozy library"
        )

    @patch("builtins.print")
    def test_inspect_room(self, mock_print: unittest.mock.Mock) -> None:
        """
        Test that inspect_room prints the room's details.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        self.player.inspect_room()
        mock_print.assert_any_call(
            "You see: A magical forest glade.", end=""
        )
        mock_print.assert_any_call("This room has 0 doors.")

    def test_get_current_room_property(self) -> None:
        """
        Test get_current_room property returns a deepcopy of the room.
        """
        current_room = self.player.get_current_room
        self.assertEqual(
            current_room.description, "A magical forest glade"
        )

        current_room.description = "A completely different room"
        self.assertNotEqual(
            self.player._current_room.description,
            current_room.description
        )


if __name__ == "__main__":
    unittest.main()
