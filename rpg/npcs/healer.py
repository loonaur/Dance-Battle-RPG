from rpg.npcs.npc import NPC
from pydantic import Field
from typing import TypeVar


Player = TypeVar("Player")


class Healer(NPC):
    """Represents a healer NPC that can restore the player's health."""

    description: str = Field(..., description="Description of the healer NPC.")

    def inspect(self) -> None:
        """Displays the description of the healer."""
        print(f"{self.description}")

    def interact(self, player: "Player") -> None:
        """
        Heals the player, restoring their health to full.

        Args:
            player: The player object whose health will be restored.
        """
        print(f"{self.description} heals you, restoring your full health!")
        player._health = 100
