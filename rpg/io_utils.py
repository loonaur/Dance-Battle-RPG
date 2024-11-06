import os
import json
from abc import abstractmethod
from pydantic import BaseModel, Field, ValidationError
from abc import ABC
from typing import Optional, TypeVar


PlayerType = TypeVar("Player")
GameType = TypeVar("Game")


class Inspectable(ABC, BaseModel):
    """Abstract base class to define inspectable game elements."""

    @abstractmethod
    def inspect(self) -> None:
        """Displays the description of the inspectable element."""
        pass


class Interactable(ABC, BaseModel):
    """Abstract base class to define interactable game elements."""

    @abstractmethod
    def interact(self, player: "PlayerType") -> None:
        """Handles interaction with the player."""
        pass


class Scanner(BaseModel):
    """Utility class to handle integer input from the player."""

    value: int = Field(0, description="Positive integer input.", ge=-1)

    def read_int(self, prompt: str = "") -> int:
        """
        Reads and validates integer input from the user.

        Args:
            prompt: A string to display as the input prompt.

        Returns:
            int: A valid positive integer input.
        """
        while True:
            user_input: str = input(prompt)
            try:
                self.value = int(user_input)
                if self.value < -1:
                    raise ValueError("No negative integers allowed.")
                return self.value
            except (ValueError, ValidationError):
                print("Invalid input. Please enter a positive integer.")


class Saver:
    """Handles saving and loading of the game state."""

    def __init__(self, save_directory: str = "savedgames") -> None:
        """
        Initializes the Saver class and sets up the save directory.

        Args:
            save_directory: The directory where
            the game save file will be stored.
        """
        self.save_directory: str = save_directory
        self.save_file: str = os.path.join(
            self.save_directory, "quicksave.json"
        )

        if not os.path.isdir(self.save_directory):
            try:
                os.makedirs(self.save_directory)
                print(f"Created save directory: {self.save_directory}")
            except OSError as e:
                print(f"Error creating directory {self.save_directory}: {e}")

    def quick_save(self, game: "GameType") -> None:
        """
        Saves the current game state to a JSON file.

        Args:
            game: The game object to be saved.
        """
        if not hasattr(game, "toJSON"):
            print("Provided object does not implement toJSON method.")
            return

        try:
            with open(self.save_file, "w") as file:
                json.dump(game.toJSON(), file, indent=4)
            print(f"Game successfully saved to {self.save_file}.")
        except Exception as e:
            print(f"An error occurred while saving the game: {e}")

    def quick_load(self) -> Optional["GameType"]:
        """
        Loads the game state from the save file, if it exists.

        Returns:
            Game: The loaded game object, or None if loading fails.
        """
        from rpg.game import Game

        if not os.path.isfile(self.save_file):
            print(f"No save file found at {self.save_file}. "
                  f"Unable to load the game.")
            return None

        try:
            with open(self.save_file, "r") as file:
                data: dict = json.load(file)
            game: Game = Game.fromJSON(data)
            print(f"Game successfully loaded from {self.save_file}.")
            return game
        except Exception as e:
            print(f"An error occurred while loading the game: {e}")
            return None
