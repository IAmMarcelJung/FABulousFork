#!/bin/python
from tqdm import tqdm
import multiprocessing
from joblib import Parallel, delayed
from typing import Dict, List

from search_path.mapping import Mapping
from search_path.node import NodeHeader
from search_path.tile import Tile
from search_path.bfs import bfs
from search_path.graph import create_graph
from search_path.utils import get_all_locations_of_tile_type, get_tiles_for_fabric
from search_path.fasm_features import append_features_to_file, create_features


features = []
cpu_cores = min(multiprocessing.cpu_count(), 16)

def search_in_tile(graph: Dict, tile: Tile, start: str, end: str, mapping: Mapping) -> List:
    """Search all possible paths inside a given tile.

    :param Dict graph: The graph in which to search.
    :param Tile tile: The tile in which to search.
    :param str start: The name of the start node.
    :param str end: The name of the end node.
    :return The list of shortest paths from start to end.
    :rtype List
    """
    start_node = NodeHeader(start, tile)
    end_node = NodeHeader(end, tile)
    paths = bfs(graph, start_node, end_node, mapping)
    return paths

start = "LA_O"
end = "LA_I3"
pip_file = "tb_test/.FABulous/pips.txt"
fabric_file = "search_path/fabric.csv"
tile_type = Tile.Types.LUT4AB
#tile_type = Tile.Types.RAM_IO
mapping = Mapping()
graph = create_graph(pip_file, mapping)
test = NodeHeader(start, Tile(1,1))

tiles = get_tiles_for_fabric(fabric_file)
tiles = get_all_locations_of_tile_type(tile_type, tiles)
#tiles = tiles[:10]

print("Searching for possible paths:")
paths = list(
    tqdm(
        Parallel(return_as="generator", n_jobs=cpu_cores)(
            delayed(search_in_tile)(graph, tile, start, end, mapping) for tile in tiles
        ),
        total=len(tiles),
    )
)
features = []
for path in paths:
    first_path = path[0]
    header_node_path = mapping.uid_path_to_node_header_path(first_path)
    features += create_features(header_node_path)

append_features_to_file(features, "test_append.txt")
