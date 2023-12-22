#!/bin/python
from tqdm import tqdm
import multiprocessing
import joblib
from joblib import Parallel, delayed
from search_path.graph import *
from search_path.utils import *
from search_path.mapping import *


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
#print(tile_type)
mapping = Mapping()
graph = create_graph_for_all_tiles_of_type(fabric_file, pip_file, tile_type, mapping)
test = NodeHeader(start, Tile(1,1))
print(mapping.uid_to_node_header)

tiles = get_tiles_for_fabric(fabric_file)
tiles = get_all_locations_of_tile_type(tile_type, tiles)
tiles = tiles[:10]

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
    #print(path)
    features += create_features(path[0])

append_features_to_file(features, "test_append.txt")
