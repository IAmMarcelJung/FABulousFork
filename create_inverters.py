#!/bin/python3
import multiprocessing
import argparse
import os

from joblib import Parallel, delayed
from tqdm import tqdm
from typing import Dict, List

from search_path.mapping import Mapping
from search_path.node import NodeHeader
from search_path.tile import Tile
from search_path.bfs import bfs
from search_path.graph import create_graph
from search_path.utils import get_all_locations_of_tile_type, get_tiles_for_fabric, convert_and_sort
from search_path.fasm_features import append_features_to_file, create_features

def search_in_tile(graph: Dict, tile: Tile, start: str, end: str, mapping: Mapping) -> List:
    """Search all possible paths inside a given tile.

    :param Dict graph: The graph in which to search.
    :param Tile tile: The tile in which to search.
    :param str start: The name of the start node.
    :param str end: The name of the end node.
    :return: The list of shortest paths from start to end.
    :rtype: List
    """
    start_node = NodeHeader(start, tile)
    end_node = NodeHeader(end, tile)
    paths = bfs(graph, start_node, end_node, mapping)
    return paths

def parse_arguments():
    parser = argparse.ArgumentParser(
            prog='create_inverters',
            description='Create inverters in a FABulous fabric.',
            epilog='Text at the bottom of help')
    parser.add_argument("directory", help="Path to the project directory")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error {directory_path} not found")
        exit(1)
    return args


if __name__ == "__main__":

    cpu_cores = min(multiprocessing.cpu_count(), 32)
    print(f"Using {cpu_cores} cores")
    args = parse_arguments()
    project_directory = args.directory
    luts_in_tile = ["A", "B", "C", "D", "E", "F", "G", "H"]
    pip_file = f"{project_directory}/.FABulous/pips.txt"
    fabric_file = f"{project_directory}/fabric.csv"
    tile_type = Tile.Types.LUT4AB
    #tile_type = Tile.Types.RAM_IO
    mapping = Mapping()

    print("Creating graph...")
    graph = create_graph(pip_file, mapping)
    for key in graph.keys():
        if graph.uid_to_node_header[key] == "A_O":
            print("FOUND A_O")

    tiles = get_tiles_for_fabric(fabric_file)
    tiles = get_all_locations_of_tile_type(tile_type, tiles)
    tiles = tiles[:1]

    paths = []
    print("Searching for possible paths:")
    for lut in tqdm(luts_in_tile):
        start = f"L{lut}_O"
        end = f"L{lut}_I3"
        tmp_paths = list(
                tqdm(
                    Parallel(return_as="generator", n_jobs=cpu_cores)(
                        delayed(search_in_tile)(graph, tile, start, end, mapping) for tile in tiles
                    ),
                    total=len(tiles),
                )
            )
        for tmp_path in tmp_paths:
            paths.append(tmp_path)

    print(paths)
    header_node_paths = convert_and_sort(paths, mapping)
    print(header_node_paths)
    features = []
    used_tiles = set()
    for path in header_node_paths:
        features += create_features(path, used_tiles)


    try:
        append_features_to_file(features, f"{project_directory}/user_design/sequential_16bit_en.fasm")
    except(FileNotFoundError) as e:
        print(f"Error: {e}")
        exit(1)


