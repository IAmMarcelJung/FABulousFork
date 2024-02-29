import unittest
from search_path.utils import get_all_locations_of_tile_type


class TestGetAllLocationsOfTileType(unittest.TestCase):

    def test_empty_tiles(self):
        """Test when tiles dictionary is empty."""
        # Arrange
        tiles = {}

        # Act
        result = get_all_locations_of_tile_type("grass", tiles)

        # Assert
        self.assertEqual(result, [])

    def test_no_matching_tile_type(self):
        """Test when there is no matching tile type in the tiles dictionary."""
        # Arrange
        tiles = {"A": "water", "B": "sand", "C": "rock"}

        # Act
        result = get_all_locations_of_tile_type("grass", tiles)

        # Assert
        self.assertEqual(result, [])

    def test_single_matching_location(self):
        """Test when there is one location with the specified tile type."""
        # Arrange
        tiles = {"A": "grass", "B": "sand", "C": "rock"}

        # Act
        result = get_all_locations_of_tile_type("grass", tiles)

        # Assert
        self.assertEqual(result, ["A"])

    def test_multiple_matching_locations(self):
        """Test when there are multiple locations with the specified tile type."""
        # Arrange
        tiles = {"A": "grass", "B": "grass", "C": "rock", "D": "grass"}

        # Act
        result = get_all_locations_of_tile_type("grass", tiles)

        # Assert
        self.assertEqual(result, ["A", "B", "D"])

    def test_case_sensitive_matching(self):
        """Test case-sensitive matching of tile type."""
        # Arrange
        tiles = {"A": "Grass", "B": "grass", "C": "GRASS"}

        # Act
        result = get_all_locations_of_tile_type("grass", tiles)

        # Assert
        self.assertEqual(result, ["B"])

    def test_mixed_types(self):
        """Test when there are multiple tile types in the tiles dictionary."""
        # Arrange
        tiles = {"A": "grass", "B": "water", "C": "sand", "D": "grass"}

        # Act
        result = get_all_locations_of_tile_type("grass", tiles)

        # Assert
        self.assertEqual(result, ["A", "D"])

    def test_tile_type_not_string(self):
        """Test when the tile type is not a string."""
        # Arrange
        tiles = {"A": 123, "B": "grass", "C": "rock"}

        # Act and Assert
        with self.assertRaises(TypeError):
            get_all_locations_of_tile_type("grass", tiles)

    def test_empty_tile_type(self):
        """Test when the tile type is an empty string."""
        # Arrange
        tiles = {"A": "grass", "B": "sand", "C": "rock"}

        # Act and Assert
        with self.assertRaises(ValueError):
            get_all_locations_of_tile_type("", tiles)

    def test_none_tile_type(self):
        """Test when the tile type is None."""
        # Arrange
        tiles = {"A": "grass", "B": "sand", "C": "rock"}

        # Act and Assert
        with self.assertRaises(ValueError):
            get_all_locations_of_tile_type(None, tiles)

    def test_none_tiles(self):
        """Test when the tiles dictionary is None."""
        # Arrange

        # Act and Assert
        with self.assertRaises(ValueError):
            get_all_locations_of_tile_type("grass", None)


if __name__ == "__main__":
    unittest.main()
