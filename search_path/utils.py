#!/bin/python
import os
from typing import *
from search_path.tile import *


def transpose_csv(input_file, output_file):
    if os.path.isfile(output_file):
        return
    with open(input_file, "r") as f_in:
        a = zip(*csv.reader(f_in))

    with open(output_file, "w") as f_out:
        csv.writer(f_out).writerows(a)

def create_data(project_dir):
    pip_file = project_dir + ".FABulous/pips.txt"
    with open(pip_file, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            line_list = line.split(",")
            tile = line_list[0]
            feature = line_list[-1]

def get_tiles_for_fabric(fabric_file: str):
    """
    Read the fabric.csv file and assign the type of tile to the position.
    """
    tiles = {}
    with open(fabric_file) as f:
        for y, line in enumerate(f):
            if line.startswith("FabricBegin"):
                continue
            if line.startswith("FabricEnd"):
                break
            line_list = line.split(",")
            tile_list = []
            for elem in line_list:
                if elem == "":
                    break
                tile_list.append(elem)
            for x, tile in enumerate(tile_list):
                tiles.update({Tile(x, y-1): tile})
    return tiles

def get_all_locations_of_tile_type(tile_type: str, tiles: Dict):
    """
    Get all locations of the specified tile type.
    """
    # Check if tile_type is a non-empty string
    if not isinstance(tile_type, str) or not tile_type:
        raise ValueError("Invalid tile type")

    # Check if tiles is a dictionary
    if not isinstance(tiles, dict) or tiles is None:
        raise ValueError("Invalid tiles dictionary")

    locations = []
    for key, value in tiles.items():
        if not isinstance(value, str):
            raise TypeError("Invalid tile type in tiles dictionary")
        #if tiles[key] == tile_type:
        if value == tile_type:
            locations.append(key)

    return locations

def get_all_locations_of_tiles(tiles: Dict):
    """
    Get all locations of all tiles.
    """
    locations = []
    for key in tiles.keys():
        if tiles[key] not in [Tile.Types.N_term_RAM_IO, Tile.Types.RAM_IO, Tile.Types.S_term_RAM_IO]:
            locations.append(key)
    return locations

if __name__ == "__main__":
    pass
