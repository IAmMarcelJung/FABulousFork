#!/bin/python
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Tile:
    """Defines a tile with an x any a y coordinate."""

    x: int
    y: int

    def to_string(self):
        """Create a string from a tile.

        :param Tile tile: The tile to be turned into a string.
        :return: The tile converted to a string
        :rtype: str
        """
        return f"X{self.x}Y{self.y}"

    class Types(str, Enum):
        """Definition of all available tile types."""

        NULL = "NULL"
        LUT4AB = "LUT4AB"
        W_IO = "W_IO"
        RegFile = "RegFile"
        DSP_bot = "DSP_bot"
        DSP_top = "DSP_top"
        RAM_IO = "RAM_IO"
        N_term_single = "N_term_single"
        N_term_single2 = "N_term_single2"
        N_term_DSP = "N_term_DSP"
        N_term_RAM_IO = "N_term_RAM_IO"
        S_term_single = "S_term_single"
        S_term_single2 = "S_term_single2"
        S_term_DSP = "S_term_DSP"
        S_term_RAM_IO = "S_term_RAM_IO"


def create_tile_from_string(tile_str: str) -> Tile:
    """Create a tile from a string.

    :param str tile_str: The tile as a string to be converted.
    :return: The tile string converted to a Tile.
    :rtype: Tile
    """
    parts = tile_str.split("Y")
    x = parts[0].strip("X")
    y = parts[1].strip("Y")
    return Tile(int(x), int(y))


if __name__ == "__main__":
    pass
