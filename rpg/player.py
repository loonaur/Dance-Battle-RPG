from pydantic import BaseModel, Field, PrivateAttr
from copy import deepcopy
from rpg.room import Room
from typing import Dict, Any, Optional
from rpg.io_utils import Scanner


class Player(BaseModel):
    """Represents the player character and manages player interactions."""

    name: str = Field(..., description="Player username.")
    _current_room: Optional[Room] = PrivateAttr(default_factory=str)
    _health: int = PrivateAttr(default=100)

    def enter_room(self, room: Room) -> None:
        """
        Moves the player into the specified room.

        Args:
            room: The Room object the player will enter.
        """
        self._current_room = room

    def inspect_room(self) -> None:
        """
        Inspects the current room, displaying its details.

        Prints the room's description and other available options.
        """
        if self._current_room:
            self._current_room.inspect()
        else:
            print(f"{self.name} is not in any room.")

    def look_for_way_out(self, scanner: Scanner) -> None:
        """
        Lists all doors in the current room and lets the player choose one.

        Allows the player to select a door to explore new rooms.
        """
        if self._current_room:
            self._current_room.list_doors()
            door_choice: int = scanner.read_int("Choose a door by index: ")
            if 0 <= door_choice < len(self._current_room.doors):
                selected_door = self._current_room.doors[door_choice]
                selected_door.interact(self)
            else:
                print("Invalid door selection. Please choose a valid door.")
        else:
            print(f"{self.name} is not in any room.")

    def look_for_company(self) -> None:
        """
        Lists all NPCs present in the current room.

        Allows the player to see who else is in the room.
        """
        if self._current_room:
            self._current_room.list_npcs()
        else:
            print(f"{self.name} is not in any room.")

    def player_death(self) -> str:
        """
        Handles player death and restores health.

        Returns:
            str: "DEAD" to notify that the player has died and the game
            will restart.
        """
        print("\nThe game will restart. Your full health will be restored.")
        self._health = 100
        return "DEAD"

    @property
    def get_current_room(self) -> Room:
        """
        Retrieves the player's current room.

        Returns:
            Room: The Room object representing the player's current location.
        """
        return deepcopy(self._current_room)

    def toJSON(self) -> Dict[str, Any]:
        """
        Converts the player's state to a JSON-compatible dictionary.

        Returns:
            Dict[str, Any]: A dictionary representing the player's state.
        """
        return {
            "name": self.name,
            "current_room": (
                self._current_room.toJSON()
                if self._current_room
                else None
            )
        }

    @classmethod
    def fromJSON(cls, data: Dict[str, Any]) -> 'Player':
        """
        Creates a Player instance from a JSON-compatible dictionary.

        Args:
            data: A dictionary containing player data.

        Returns:
            Player: A Player object initialized from the provided data.
        """
        player = cls(name=data['name'])
        if data.get("current_room"):
            player.enter_room(Room.fromJSON(data["current_room"]))
        return player
