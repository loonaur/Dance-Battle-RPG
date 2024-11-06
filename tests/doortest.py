import unittest
from unittest.mock import patch, MagicMock
from rpg.room.door import Door


class TestDoor(unittest.TestCase):
    """
    Unit tests for the Door class and its methods.
    """

    def setUp(self) -> None:
        """Set up test objects and mocks."""
        self.door_wooden = Door(description="Wooden Door", leads_to=None)

        self.mock_room = MagicMock()
        self.mock_room.description = "Mystery Room"

        self.door_magic = Door(
            description="Magic Door",
            leads_to=self.mock_room
        )

        self.mock_player = MagicMock()
        self.mock_player._current_room = MagicMock(
            description="Starting Room"
        )

    @patch("builtins.print")
    def test_inspect_method(self, mock_print: unittest.mock.Mock) -> None:
        """
        Test that the inspect method prints the correct description.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        self.door_wooden.inspect()
        mock_print.assert_called_once_with(
            "door description: Wooden Door"
        )

    @patch("builtins.print")
    def test_interact_with_door_without_destination(
        self, mock_print: unittest.mock.Mock
    ) -> None:
        """
        Test interaction with a door that does not lead anywhere.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        self.door_wooden.interact(self.mock_player)
        mock_print.assert_called_once_with(
            "The Wooden Door doesn’t seem to lead anywhere."
        )

    @patch("builtins.print")
    def test_interact_with_door_with_destination(
        self, mock_print: unittest.mock.Mock
    ) -> None:
        """
        Test interaction with a door that has a destination.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        self.door_magic.interact(self.mock_player)
        self.mock_player.enter_room.assert_called_once_with(self.mock_room)

        mock_print.assert_any_call("You go through Magic Door.")
        mock_print.assert_any_call(
            f"You are now in: {self.mock_player._current_room.description}"
        )

    def test_to_json(self) -> None:
        """Test the toJSON method for serialization."""
        door_data = self.door_wooden.toJSON()
        self.assertEqual(door_data["description"], "Wooden Door")
        self.assertIsNone(door_data["leads_to"])

    def test_to_json_with_destination(self) -> None:
        """Test the toJSON method for a door that leads to a room."""
        door_data = self.door_magic.toJSON()
        self.assertEqual(door_data["description"], "Magic Door")
        self.assertEqual(door_data["leads_to"], "Mystery Room")

    def test_from_json(self) -> None:
        """Test the fromJSON method for deserialization."""
        json_data = {"description": "Stone Door", "leads_to": None}
        new_door = Door.fromJSON(json_data)
        self.assertEqual(new_door.description, "Stone Door")
        self.assertIsNone(new_door.leads_to)

    def test_from_json_with_destination(self) -> None:
        """
        Test deserialization with a door that has a destination.
        """
        json_data = {
            "description": "Secret Door",
            "leads_to": "Hidden Chamber"
        }
        new_door = Door.fromJSON(json_data)
        self.assertEqual(new_door.description, "Secret Door")
        self.assertEqual(new_door.leads_to, "Hidden Chamber")


if __name__ == "__main__":
    unittest.main()
