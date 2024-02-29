import unittest

from context import modules
from modules.tile import Tile, create_tile_from_string


class TestTile(unittest.TestCase):

    def test_create_tile_from_string(self):
        """
        Test the conversion from a string to a tile.
        """
        # Act
        tile = create_tile_from_string("X1Y1")
        # Assert
        self.assertEqual(tile.x, 1)
        self.assertEqual(tile.y, 1)
        # Act
        tile = create_tile_from_string("X12Y13")
        # Assert
        self.assertEqual(tile.x, 12)
        self.assertEqual(tile.y, 13)

    def test_tile_to_str(self):
        """
        Test the conversion from a tile to a string.
        """
        # Arrange
        tile = Tile(1, 1)
        # Act
        tile_str = tile.to_string()
        # Assert
        self.assertEqual("X1Y1", tile_str)
        # Arrange
        tile = Tile(999, 999)
        # Act
        tile_str = tile.to_string()
        # Assert
        self.assertEqual("X999Y999", tile_str)


if __name__ == "__main__":
    unittest.main()
