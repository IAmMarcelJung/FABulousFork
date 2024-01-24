#!/bin/python3
import multiprocessing
import argparse
import os
import copy
import pickle

from joblib import Parallel, delayed
from tqdm import tqdm
from typing import Dict, List

from search_path.mapping import Mapping
from search_path.node import NodeHeader
from search_path.tile import Tile
from search_path.bfs import bfs
from search_path.graph import create_graph
from search_path.utils import get_all_locations_of_tile_type, get_tiles_for_fabric, convert_paths, sort_list_by_tile
from search_path.fasm_features import append_features_to_file, create_features_with_gnd_and_init, create_features

def parse_arguments():
    """
    Parse the command line arguments.

    :return: The arguments as a namespace.
    :rtype: argarse.Namespace
    """
    parser = argparse.ArgumentParser(
            prog='create_inverters',
            description='Create inverters in a FABulous fabric.')
    parser.add_argument("directory", help="Path to the project directory.")
    parser.add_argument("-t", type=int, default=1, help="Number of tiles to skip.")
    parser.add_argument("-l", type=int, default=1, help="Number of LUTs to skip.")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error {directory_path} not found")
        exit(1)
    return args

def get_max_column_number(tiles: List):
    """
    Get the maximum column number from a list of tiles.

    :param List tiles: The list of tiles.
    :return: The maximum column number.
    :rtype: int
    """
    tile_columns = []
    max_column = 0
    for tile in tiles:
        if tile.y == 1:
            if tile.x > max_column:
                max_column = tile.x
            tile_columns.append(tile.x)
    return max_column

def connect_tiles_in_top_row(max_column_number: int, existing_paths: List, graph: Dict, mapping: Mapping):
    """
    Connect all tiles in the top row.

    :param int max_column_number: The maximum column number in the fabric.
    :param List existing_paths: The list of already existing paths.
    :param Dict graph: The graph containing all nodes.
    :param Mapping mapping: The mapping from UID to NodeHeader.
    """
    for x in range(1, max_column_number):
        start_tile = Tile(x, 1)
        start_node = NodeHeader("E1BEG0", start_tile)

        end_tile = Tile(x+1, 1)
        end_node = NodeHeader("E1END0", end_tile)

        possible_paths = bfs(graph, start_node, end_node, mapping)

        path = possible_paths[0]
        existing_paths.append(path)

    for x in range(1, max_column_number):
        start_tile = Tile(x, 1)
        start_node = NodeHeader("E1END0", start_tile)

        end_tile = Tile(x, 1)
        end_node = NodeHeader("E1BEG0", end_tile)

        possible_paths = bfs(graph, start_node, end_node, mapping)

        path = possible_paths[0]
        existing_paths.append(path)
def find_paths_in_tile(tile: Tile, graph: Dict, mapping: Mapping):
    """
    Find the paths in a tile.

    :param Tile tile: The tile in which to find the paths.
    :param Dict graph: The graph containing all nodes.
    :param Mapping mapping: The mapping between UID and NodeHeader.
    """
    previous_paths = []
    inverter_paths = []
    enable_paths = []
    for lut in luts_in_tile:
        # Inverter routing
        start = f"L{lut}_O"
        end = f"L{lut}_I3"
        start_node = NodeHeader(start, tile)
        end_node = NodeHeader(end, tile)
        possible_paths = bfs(graph, start_node, end_node, mapping)
        path = possible_paths[0]
        inverter_paths.append(path)

        # Routing for the inverter enable path
        '''
        start = f"A_O"
        if not created_input:
            start_tile = Tile(0, 1)
        elif lut == "A":
            start_tile = previous_tile
        else:
            start_tile =  tile
        '''
        possible_paths = []
        previous_path_internal_index = -2
        previous_path_index = -1
        while not possible_paths:
            if previous_paths and previous_paths[previous_path_index]:
                # Check if there are nodes left to be checked in the previous_path at index previous_path_index
                if len(previous_paths[previous_path_index]) > abs(previous_path_internal_index):
                    start_node = mapping.uid_to_node_header[previous_paths[previous_path_index][previous_path_internal_index]]
                    name = start_node.name.replace("3", "0")
                    start_node_tile = start_node.tile
                    start_node = NodeHeader(name, start_node_tile)
                    previous_path_internal_index -= 1
                # No nodes left in the previous_path at index previous_path_index, decrement index to get the path before
                else:
                    previous_path_index -= 1
                    previous_path_internal_index = -2
                    start_node = mapping.uid_to_node_header[previous_paths[previous_path_index][previous_path_internal_index]]
                    name = start_node.name.replace("3", "0")
                    start_node_tile = start_node.tile
                    start_node = NodeHeader(name, start_node_tile)
            else:
                start_node = NodeHeader("E1END0", tile)

            end_node_name = end_node.name.replace("3", "0")
            end_node_tile = end_node.tile
            end_node = NodeHeader(end_node_name, end_node_tile)
            end_tile = tile
            possible_paths = bfs(graph, start_node, end_node, mapping)
            if possible_paths:
                path = possible_paths[0]
                previous_paths.append(path)

        enable_paths.append(path)
    return (inverter_paths, enable_paths)

def get_graph_and_mapping(project_dir: str):
    """
    Get the graph either from the function or the previously stored file.
    :param str project_dir: The current project directory.
    :return: The graph constructed from either the function or the file.
    :rtype: Dict
    """
    mapping = Mapping()
    path = project_dir + "data.pkl"
    #TODO: Try to check if the fabric has changed, so the graph has to be recreated
    if os.path.exists(path) :
        print("Previously_created data found, reading it...")
        with open(path, 'rb') as file:
            data = pickle.load(file)
            graph = data["graph"]
            mapping = data["mapping"]
    else:
        print("No previously created data found, creating graph and mapping...")
        graph = create_graph(pip_file, mapping)
        data = {}
        data.update({"graph": graph})
        data.update({"mapping": mapping})
        print(f"Storing graph in: {path}")
        with open(path, 'wb') as file:
            pickle.dump(data, file)
    return graph, mapping

if __name__ == "__main__":

    # Prepare variables
    cpu_cores = min(multiprocessing.cpu_count(), 32)

    args = parse_arguments()
    project_directory = args.directory
    skip_tiles = args.t
    skip_luts = args.l

    luts_in_tile = ["A", "B", "C", "D", "E", "F", "G", "H"]
    luts = luts_in_tile[::skip_luts]
    pip_file = f"{project_directory}/.FABulous/pips.txt"
    fabric_file = f"{project_directory}/fabric.csv"

    tile_type = Tile.Types.LUT4AB

    # Get the graph, the mapping and the tiles
    graph, mapping = get_graph_and_mapping(project_directory)

    tiles = get_tiles_for_fabric(fabric_file)
    tiles = get_all_locations_of_tile_type(tile_type, tiles)
    tiles = tiles[::skip_tiles]

    # Find the paths
    inverter_paths = []
    enable_paths = []
    paths = []
    print("Searching for possible paths:")
    '''
    paths += list(
            tqdm(
                Parallel(return_as="generator", n_jobs=cpu_cores)(
                    delayed(find_paths_in_tile)(tile, graph, mapping) for tile in tiles
                ),
                total=len(tiles),
            )
        )

    '''
    for tile in tqdm(tiles):
        tmp_inverter_paths, tmp_enable_paths = find_paths_in_tile(tile, graph, mapping)
        inverter_paths.append(tmp_inverter_paths[0])
        enable_paths.append(tmp_enable_paths[0])

    max_column_number = get_max_column_number(tiles)

    connect_tiles_in_top_row(max_column_number, enable_paths, graph, mapping)

    header_node_paths_inverter = convert_paths(inverter_paths, mapping)
    header_node_paths_enable = convert_paths(enable_paths, mapping)

    header_node_paths_inverter.sort(key=lambda inner_list: (inner_list[0].tile.x, inner_list[0].tile.y))

    # Add the features
    features = []
    used_tiles = set()

    for path in header_node_paths_inverter:
        features += create_features_with_gnd_and_init(path, used_tiles)

    for path in header_node_paths_enable:
        features += create_features(path, used_tiles)

    try:
        append_features_to_file(features, f"{project_directory}/user_design/sequential_16bit_en.fasm")
    except(FileNotFoundError) as e:
        print(f"Error: {e}")
        exit(1)
