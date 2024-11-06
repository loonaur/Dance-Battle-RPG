from pydantic import Field
from rpg.io_utils import Inspectable
from rpg.room.door import Door
from typing import List, Dict, Any
from rpg.npcs.npc import NPC
from rpg.json import JsonSerializable


class Room(Inspectable, JsonSerializable):
    """Represents a room in the game containing doors and NPCs."""

    description: str = Field(..., description="Room description.")
    doors: List[Door] = Field(
        default_factory=list, description="List of doors in the room."
    )
    npcs: List[NPC] = Field(
        default_factory=list, description="List of NPCs present in the room."
    )

    def inspect(self) -> None:
        """
        Displays the room's description and the number of doors.

        Prints the description and the count of doors in the current room.
        """
        print(f"You see: {self.description}.", end="")
        n_doors: int = len(self.doors)
        if n_doors == 1:
            print("This room has 1 door.")
        else:
            print(f"This room has {n_doors} doors.")

    def list_doors(self) -> None:
        """
        Lists all the doors in the room with their descriptions.

        Prompts the player to select a door by index to interact with.
        """
        print("You look around for doors. "
              "Which one do you want to go through?")
        for index, door in enumerate(self.doors):
            print(f"  ({index}) {door.description}")

    def list_npcs(self) -> None:
        """
        Lists all NPCs present in the room.

        Displays a list of NPC descriptions
        or a message if no NPCs are present.
        """
        if not self.npcs:
            print("There is no one else here.")
        else:
            print("You look if there’s someone here. You see:")
            for index, npc in enumerate(self.npcs):
                print(f"  ({index}) {npc.description}")

    def add_door(self, door: Door) -> None:
        """
        Adds a new door to the room.

        Args:
            door: The Door object to be added to the room's doors list.
        """
        self.doors.append(door)

    def add_npc(self, npc: NPC) -> None:
        """
        Adds a new NPC to the room.

        Args:
            npc: The NPC object to be added to the room's NPC list.
        """
        self.npcs.append(npc)

    def toJSON(self) -> Dict[str, Any]:
        """
        Converts the room's state to a JSON-compatible dictionary.

        Returns:
            Dict[str, Any]: A dictionary representing the room's state.
        """
        return {
            "description": self.description,
            "doors": [door.toJSON() for door in self.doors],
            "npcs": [npc.toJSON() for npc in self.npcs]
        }

    @classmethod
    def fromJSON(cls, data: Dict[str, Any]) -> 'Room':
        """
        Creates a Room instance from a JSON-compatible dictionary.

        Args:
            data: A dictionary containing room data.

        Returns:
            Room: A Room object initialized from the provided data.
        """
        room = cls(description=data['description'])
        room.doors = [Door.fromJSON(door_data)
                      for door_data in data.get("doors", [])]
        room.npcs = [NPC.fromJSON(npc_data)
                     for npc_data in data.get("npcs", [])]
        return room
