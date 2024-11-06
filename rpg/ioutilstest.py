import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
from rpg.io_utils import Inspectable, Interactable, Scanner, Saver
from typing import Any


class MockInspectable(Inspectable):
    """Mock class for Inspectable to test the abstract methods."""

    def inspect(self) -> None:
        print(f"Inspecting {self}")


class MockInteractable(Interactable):
    """Mock class for Interactable to test the abstract methods."""

    def interact(self, player: Any) -> None:
        print(f"Interacting with {player}")


class TestInspectable(unittest.TestCase):
    """Tests for the Inspectable class."""

    def test_inspect_method(self) -> None:
        """Test the inspect method of a mock inspectable object."""
        mock_inspectable = MockInspectable()
        with patch("builtins.print") as mock_print:
            mock_inspectable.inspect()
            mock_print.assert_called_once_with(
                f"Inspecting {mock_inspectable}"
            )


class TestInteractable(unittest.TestCase):
    """Tests for the Interactable class."""

    def test_interact_method(self) -> None:
        """Test the interact method of a mock interactable object."""
        mock_interactable = MockInteractable()
        player = MagicMock()
        with patch("builtins.print") as mock_print:
            mock_interactable.interact(player)
            mock_print.assert_called_once_with(
                f"Interacting with {player}"
            )


class TestScanner(unittest.TestCase):
    """Tests for the Scanner class."""

    @patch("builtins.input", side_effect=["10"])
    def test_read_int_valid(self, _) -> None:
        """Test Scanner's read_int method with valid input."""
        scanner = Scanner()
        result = scanner.read_int("Enter a number: ")
        self.assertEqual(result, 10)

    @patch("builtins.input", side_effect=["-2", "5"])
    def test_read_int_invalid_then_valid(self, _) -> None:
        """
        Test Scanner's read_int method with invalid and
        then valid input.
        """
        scanner = Scanner()
        with patch("builtins.print") as mock_print:
            result = scanner.read_int("Enter a number: ")
            self.assertEqual(result, 5)
            mock_print.assert_called_once_with(
                "Invalid input. Please enter a positive integer."
            )

    @patch("builtins.input", side_effect=["abc", "10"])
    def test_read_int_non_integer_input(self, _) -> None:
        """
        Test Scanner's read_int method with non-integer input
        followed by valid input.
        """
        scanner = Scanner()
        with patch("builtins.print") as mock_print:
            result = scanner.read_int("Enter a number: ")
            self.assertEqual(result, 10)
            mock_print.assert_called_once_with(
                "Invalid input. Please enter a positive integer."
            )


class TestSaver(unittest.TestCase):
    """Tests for the Saver class."""

    @patch("os.path.isdir", return_value=False)
    @patch("os.makedirs")
    @patch("builtins.print")
    def test_saver_init_creates_directory(self, mock_print,
                                          mock_makedirs, _) -> None:
        """Test Saver initialization when save directory does not exist."""
        Saver(save_directory="savedgames")
        mock_makedirs.assert_called_once_with("savedgames")
        mock_print.assert_called_once_with(
            "Created save directory: savedgames"
        )

    @patch("os.path.isdir", return_value=True)
    def test_saver_init_no_directory_creation(self, mock_isdir) -> None:
        """Test Saver initialization when save directory exists."""
        Saver(save_directory="savedgames")
        mock_isdir.assert_called_once_with("savedgames")

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_quick_save_successful(self, mock_print, mock_json_dump,
                                   mock_file) -> None:
        """Test Saver's quick_save method when saving is successful."""
        mock_game = MagicMock()
        mock_game.toJSON.return_value = {"game": "state"}
        saver = Saver()
        saver.quick_save(mock_game)
        mock_file.assert_called_once_with(
            os.path.join("savedgames", "quicksave.json"), "w"
        )
        mock_json_dump.assert_called_once_with(
            {"game": "state"}, mock_file(), indent=4
        )
        mock_print.assert_called_once_with(
            "Game successfully saved to savedgames/quicksave.json."
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump", side_effect=Exception("Save error"))
    @patch("builtins.print")
    def test_quick_save_exception(self, mock_print, _, __) -> None:
        """
        Test Saver's quick_save method when an error occurs
        during saving.
        """
        mock_game = MagicMock()
        mock_game.toJSON.return_value = {"game": "state"}
        saver = Saver()
        saver.quick_save(mock_game)
        mock_print.assert_called_once_with(
            "An error occurred while saving the game: Save error"
        )

    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open,
           read_data='{"game": "state"}')
    @patch("json.load")
    @patch("builtins.print")
    def test_quick_load_successful(self, mock_print, _, __, ___) -> None:
        """Test Saver's quick_load method when loading is successful."""
        mock_game_class = MagicMock()
        mock_game_class.fromJSON.return_value = "Loaded Game"
        with patch("rpg.game.Game", mock_game_class):
            saver = Saver()
            result = saver.quick_load()
            mock_print.assert_called_once_with(
                "Game successfully loaded from savedgames/quicksave.json."
            )
            self.assertEqual(result, "Loaded Game")

    @patch("os.path.isfile", return_value=False)
    @patch("builtins.print")
    def test_quick_load_no_save_file(self, mock_print, _) -> None:
        """Test Saver's quick_load method when no save file exists."""
        result = Saver().quick_load()
        mock_print.assert_called_once_with(
            "No save file found at savedgames/quicksave.json. "
            "Unable to load the game."
        )
        self.assertIsNone(result)

    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open,
           read_data='{"game": "state"}')
    @patch("json.load", side_effect=Exception("Load error"))
    @patch("builtins.print")
    def test_quick_load_exception(self, mock_print, _, __, ___) -> None:
        """
        Test Saver's quick_load method when an error occurs
        during loading.
        """
        result = Saver().quick_load()
        mock_print.assert_called_once_with(
            "An error occurred while loading the game: Load error"
        )
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
