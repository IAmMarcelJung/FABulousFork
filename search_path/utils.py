#!/bin/python
import os
import csv

from typing import Dict, List
from search_path.tile import Tile
from search_path.mapping import Mapping


def transpose_csv(input_file, output_file):
    if os.path.isfile(output_file):
        return
    with open(input_file, "r") as f_in:
        a = zip(*csv.reader(f_in))

    with open(output_file, "w") as f_out:
        csv.writer(f_out).writerows(a)

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

def convert_and_sort(paths: List, mapping: Mapping):
    """
    Convert paths to the node header representation and sort the path list according to the tile"
    :param List paths: The list of possible paths.
    :param Mapping mapping: The mapping between node header and UID.
    :return: The converted and sorted path list.
    :rtype: List

    """
    header_node_paths = []
    for path in paths:
        print(path)
        if isinstance(path, list):
            header_node_path = mapping.uid_path_to_node_header_path(path[0])
            header_node_paths.append(header_node_path)

    header_node_paths.sort(key=lambda inner_list: (inner_list[0].tile.x, inner_list[0].tile.y))
    return header_node_paths

if __name__ == "__main__":
    pass
