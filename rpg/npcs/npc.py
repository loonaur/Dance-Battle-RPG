from pydantic import Field
from rpg.io_utils import Inspectable, Interactable
from typing import Dict, Any, TypeVar


Player = TypeVar("Player")


class NPC(Inspectable, Interactable):
    """Represents a non-playable character (NPC) in the game."""

    description: str = Field(..., description="NPC description.")
    interact_message: str = Field(..., description="NPC interaction message.")

    def inspect(self) -> None:
        """Displays the NPC's description."""
        print(f"{self.description}")

    def interact(self, player: 'Player') -> None:
        """
        Handles interaction with the player.

        Default interaction behavior for an inactive or non-hostile NPC.

        Args:
            player: The player object interacting with the NPC.
        """
        print(f"{self.interact_message}")

    def toJSON(self) -> Dict[str, Any]:
        """
        Converts the NPC's state to a JSON-compatible dictionary.

        Returns:
            Dict[str, Any]: A dictionary representing the NPC's state.
        """
        return {
            "description": self.description,
            "interact_message": self.interact_message
        }

    @classmethod
    def fromJSON(cls, data: Dict[str, Any]) -> 'NPC':
        """
        Creates an NPC instance from a JSON-compatible dictionary.

        Args:
            data: A dictionary containing NPC data.

        Returns:
            NPC: An NPC object initialized from the provided data.
        """
        return cls(
            description=data["description"],
            interact_message=data["interact_message"]
        )
