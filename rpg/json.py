from abc import ABC, abstractmethod
from typing import Any, Dict


class JsonSerializable(ABC):
    """An abstract base class for objects
    that can be serialized to and from JSON.

    Provides methods for converting objects to a JSON-compatible dictionary
    and reconstructing them from such dictionaries.

    Methods:
        toJSON: Serializes the object to a JSON-compatible dictionary.
        fromJSON: Reconstructs an object from a JSON-compatible dictionary.
        _is_json_serializable: Checks if a value is natively JSON serializable.
        _serialize_value: Recursively serializes values that are not natively
                          JSON serializable.
    """

    @abstractmethod
    def toJSON(self) -> Dict[str, Any]:
        """Converts the object to a JSON-compatible dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object that
            can be serialized to JSON.
        """
        pass

    @abstractmethod
    def fromJSON(cls, data: Dict[str, Any]) -> 'JsonSerializable':
        """Creates an instance of the class from a JSON-compatible dictionary.

        Args:
            data (Dict[str, Any]): The dictionary containing the object's data.

        Returns:
            JsonSerializable: An instance of the class reconstructed from the
            provided dictionary.
        """
        pass

    def _is_json_serializable(self, value: Any) -> bool:
        """Checks if a value is natively JSON serializable.

        Args:
            value (Any): The value to be checked.

        Returns:
            bool: True if the value is natively JSON serializable,
            otherwise False.
        """
        return isinstance(
            value, (int, float, str, bool, type(None), list, dict)
        )

    def _serialize_value(self, value: Any) -> Any:
        """Recursively serializes the value if
        it is not natively JSON serializable.

        This method converts non-JSON serializable values into serializable
        representations. For example, it converts `JsonSerializable` objects
        to their `toJSON` output.

        Args:
            value (Any): The value to be serialized.

        Returns:
            Any: The serialized value that can be converted into JSON.

        Raises:
            TypeError: If the value cannot be
            serialized into a JSON-compatible format.
        """
        if self._is_json_serializable(value):
            return value
        elif isinstance(value, JsonSerializable):
            return value.toJSON()
        elif isinstance(value, list):
            return [self._serialize_value(item) for item in value]
        elif isinstance(value, dict):
            return {key: self._serialize_value(val)
                    for key, val in value.items()}
        else:
            raise TypeError(f"Cannot serialize value of type {type(value)}")
