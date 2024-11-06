import unittest
from typing import Any, Dict
from rpg.json import JsonSerializable


class TestSerializableObject(JsonSerializable):
    """
    A concrete class inheriting from JsonSerializable for testing purposes.
    This class represents an object with a name and value that can be
    serialized to and from JSON.
    """

    def __init__(self, name: str, value: Any) -> None:
        """
        Initialize the test object with a name and a value.

        Args:
            name (str): The name of the object.
            value (Any): The value associated with the object.
        """
        self.name = name
        self.value = value

    def toJSON(self) -> Dict[str, Any]:
        """
        Convert the object to a JSON-compatible dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            "name": self.name,
            "value": self.value
        }

    @classmethod
    def fromJSON(cls, data: Dict[str, Any]) -> "TestSerializableObject":
        """
        Reconstruct the object from a JSON-compatible dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing the object's data.

        Returns:
            TestSerializableObject: A new instance of the object.
        """
        return cls(data["name"], data["value"])

    def is_json_serializable(self, value: Any) -> bool:
        """
        Check if the value is JSON serializable.

        Args:
            value (Any): The value to check.

        Returns:
            bool: True if the value is JSON serializable, False otherwise.
        """
        return self._is_json_serializable(value)

    def serialize_value(self, value: Any) -> Any:
        """
        Recursively serialize non-native JSON values to a JSON-compatible form.

        Args:
            value (Any): The value to serialize.

        Returns:
            Any: A JSON-compatible representation of the value.
        """
        return self._serialize_value(value)


class TestJsonSerializable(unittest.TestCase):
    """
    Unit tests for the JsonSerializable class and its implementations.
    Tests the toJSON, fromJSON, and helper methods.
    """

    def setUp(self) -> None:
        """
        Set up the test object for use in the test cases.
        """
        self.test_obj = TestSerializableObject("TestName", 123)

    def test_toJSON(self) -> None:
        """
        Test that toJSON correctly serializes an object to a JSON-compatible
        dictionary.
        """
        expected_output = {"name": "TestName", "value": 123}
        result = self.test_obj.toJSON()
        self.assertEqual(result, expected_output)

    def test_fromJSON(self) -> None:
        """
        Test that fromJSON correctly reconstructs an object from a
        JSON-compatible dictionary.
        """
        input_data = {"name": "TestName", "value": 123}
        obj = TestSerializableObject.fromJSON(input_data)
        self.assertEqual(obj.name, "TestName")
        self.assertEqual(obj.value, 123)

    def test_is_json_serializable(self) -> None:
        """
        Test that _is_json_serializable correctly identifies JSON-serializable
        values.
        """
        self.assertTrue(self.test_obj.is_json_serializable(123))
        self.assertTrue(self.test_obj.is_json_serializable("string"))
        self.assertFalse(self.test_obj.is_json_serializable(self.test_obj))

    def test_serialize_value(self) -> None:
        """
        Test that _serialize_value correctly serializes non-native JSON values
        to JSON-compatible dictionaries.
        """
        serialized_obj = self.test_obj.toJSON()
        self.assertEqual(serialized_obj, {"name": "TestName", "value": 123})


if __name__ == "__main__":
    unittest.main()
