from pydantic import Field
from rpg.io_utils import Inspectable, Interactable
from typing import Dict, Any, Optional, TypeVar


RoomType = TypeVar("Room")
PlayerType = TypeVar("Player")


class Door(Inspectable, Interactable):
    """Class for a door that connects rooms and can be interacted with.

    Attributes:
        description (str): The description of the door.
        leads_to (Optional[RoomType]): The room the door leads to, if any.
    """

    description: str = Field(..., description="door description")
    leads_to: Optional[RoomType] = Field(None, alias="leads_to")

    def inspect(self) -> None:
        """Displays the description of the door."""
        print(f"door description: {self.description}")

    def interact(self, player: "PlayerType") -> None:
        """Allows the player to interact with the door.

        Args:
            player (Player): The player who is interacting with the door.
        """
        if self.leads_to is not None:
            player.enter_room(self.leads_to)
            print(f"You go through {self.description}.")
            print(f"You are now in: {player._current_room.description}")
        else:
            print(f"The {self.description} doesn’t seem to lead anywhere.")

    def toJSON(self) -> Dict[str, Any]:
        """Serializes the Door object to a JSON-compatible dictionary.

        Returns:
            Dict[str, Any]: The serialized dictionary
            representation of the Door.
        """
        return {
            "description": self.description,
            "leads_to": (
                None if self.leads_to is None
                else self.leads_to.description
            )
        }

    @classmethod
    def fromJSON(cls, data: Dict[str, Any]) -> "Door":
        """Deserializes a Door object from a JSON-compatible dictionary.

        Args:
            data (Dict[str, Any]): The dictionary containing door data.

        Returns:
            Door: A new Door object created from the provided data.
        """
        description: str = data.get("description")
        leads_to: Optional[str] = data.get("leads_to")
        return cls(description=description, leads_to=leads_to)
