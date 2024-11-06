import unittest
from unittest.mock import MagicMock, patch
from rpg.room import Room
from rpg.door import Door
from rpg.npc import NPC


class TestRoom(unittest.TestCase):
    """
    Unit tests for the Room class and its methods.
    """

    def setUp(self) -> None:
        """Set up a basic Room instance and mock objects for testing."""
        self.mock_door1 = MagicMock(spec=Door)
        self.mock_door1.description = "A red wooden door"

        self.mock_door2 = MagicMock(spec=Door)
        self.mock_door2.description = "A blue steel door"

        self.mock_npc1 = MagicMock(spec=NPC)
        self.mock_npc1.description = "A friendly wizard"

        self.mock_npc2 = MagicMock(spec=NPC)
        self.mock_npc2.description = "A grumpy goblin"

        self.room = Room(description="A dark and spooky room")
        self.room.add_door(self.mock_door1)
        self.room.add_npc(self.mock_npc1)

    @patch("builtins.print")
    def test_inspect_method(self, mock_print: unittest.mock.Mock) -> None:
        """
        Test the inspect method prints the correct description and door count.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        self.room.inspect()
        mock_print.assert_any_call("You see: A dark and spooky room.", end="")
        mock_print.assert_any_call("This room has 1 door.")

    @patch("builtins.print")
    def test_list_doors(self, mock_print: unittest.mock.Mock) -> None:
        """
        Test that list_doors prints the correct list of doors.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        self.room.add_door(self.mock_door2)
        self.room.list_doors()
        mock_print.assert_any_call(
            "You look around for doors. Which one do you want to go through?"
        )
        mock_print.assert_any_call("  (0) A red wooden door")
        mock_print.assert_any_call("  (1) A blue steel door")

    @patch("builtins.print")
    def test_list_npcs(self, mock_print: unittest.mock.Mock) -> None:
        """
        Test that list_npcs prints the correct list of NPCs.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        self.room.add_npc(self.mock_npc2)
        self.room.list_npcs()
        mock_print.assert_any_call(
            "You look if there’s someone here. You see:"
        )
        mock_print.assert_any_call("  (0) A friendly wizard")
        mock_print.assert_any_call("  (1) A grumpy goblin")

    @patch("builtins.print")
    def test_list_npcs_when_empty(self,
                                  mock_print: unittest.mock.Mock) -> None:
        """
        Test list_npcs prints the correct message when no NPCs are present.

        Args:
            mock_print (unittest.mock.Mock): Mock for the print function.
        """
        empty_room = Room(description="An empty room")
        empty_room.list_npcs()
        mock_print.assert_called_once_with("There is no one else here.")

    def test_add_door(self) -> None:
        """Tests adding a door to the room."""
        initial_door_count = len(self.room.doors)
        new_door = MagicMock(spec=Door, description="A hidden trapdoor")
        self.room.add_door(new_door)
        self.assertEqual(len(self.room.doors), initial_door_count + 1)
        self.assertIn(new_door, self.room.doors)

    def test_add_npc(self) -> None:
        """Tests adding an NPC to the room."""
        initial_npc_count = len(self.room.npcs)
        new_npc = MagicMock(spec=NPC, description="A silent assassin")
        self.room.add_npc(new_npc)
        self.assertEqual(len(self.room.npcs), initial_npc_count + 1)
        self.assertIn(new_npc, self.room.npcs)

    def test_to_json_method(self) -> None:
        """
        Tests serialization of a Room object to a JSON-compatible dictionary.
        """
        self.mock_door1.toJSON.return_value = {
            "description": "A red wooden door"
        }
        self.mock_npc1.toJSON.return_value = {
            "description": "A friendly wizard"
        }

        room_data = self.room.toJSON()
        expected_output = {
            "description": "A dark and spooky room",
            "doors": [{"description": "A red wooden door"}],
            "npcs": [{"description": "A friendly wizard"}]
        }
        self.assertEqual(room_data, expected_output)

    def test_from_json_method(self) -> None:
        """
        Tests deserialization from a JSON-compatible dictionary to a Room
        object.
        """
        json_data = {
            "description": "A cozy cabin",
            "doors": [{"description": "A wooden front door"}],
            "npcs": [{"description": "An old man"}]
        }

        with patch("rpg.door.Door.fromJSON", return_value=self.mock_door1):
            with patch("rpg.npc.NPC.fromJSON", return_value=self.mock_npc1):
                room = Room.fromJSON(json_data)

                self.assertEqual(room.description, "A cozy cabin")
                self.assertEqual(
                    room.doors[0].description,
                    self.mock_door1.description
                )
                self.assertEqual(
                    room.npcs[0].description,
                    self.mock_npc1.description
                )


if __name__ == "__main__":
    unittest.main()
