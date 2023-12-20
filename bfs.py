#!/bin/python
from tqdm import tqdm
from search_path.graph import *
from search_path.utils import *
import multiprocessing
import joblib
from joblib import Parallel, delayed


features = []
cpu_cores = max(multiprocessing.cpu_count(), 16)

    #for y in range(1, 15)
def create_graph_for_all_tiles_of_type(fabric_file: str, pip_file: str, tile_type: str) -> Dict:
    tiles = get_tiles_for_fabric(fabric_file)
    tiles = get_all_locations_of_tile_type(tile_type, tiles)
    graph = {}
    for tile in tqdm(tiles):
        tile_graph = create_graph_for_tile(pip_file, tile)
        graph = graph | tile_graph
    return graph

def create_graph_for_tile(pip_file, tile: Tile) -> Dict:
#tile = Tile(x, y)
#target_path = [Node_Header(name='LA_O', tile=Tile(x=x, y=y)), Node_Header(name='JW2BEG1', tile=Tile(x=x, y=y)), Node_Header(name='JW2END1', tile=Tile(x=1, y=1)), Node_Header(name='J_l_AB_BEG3', tile=Tile(x=1, y=1)), Node_Header(name='J_l_AB_END3', tile=Tile(x=1, y=1)), Node_Header(name='LA_I3', tile=Tile(x=1, y=1))]
    nodes = get_nodes_from_file_for_tile(pip_file, tile)
    graph = add_parents_and_children(pip_file, tile, nodes)
    return graph

def search_in_tile(graph: Dict, tile: Tile, start: str, end: str):
    start_node = Node_Header(start, tile)
    end_node = Node_Header(end, tile)
    paths = bfs(graph, start_node, end_node)
    features = []
    if paths:
        features += create_features(paths[0])
    return features

start = "LA_O"
end = "LA_I3"
pip_file = "tb_test/.FABulous/pips.txt"
fabric_file = "search_path/fabric.csv"
tile_type = "LUT4AB"
graph = create_graph_for_all_tiles_of_type(fabric_file, pip_file, tile_type)
test = Node_Header(start, Tile(1,1))

tiles = get_tiles_for_fabric(fabric_file)
tiles = get_all_locations_of_tile_type(tile_type, tiles)

print(Parallel(n_jobs=cpu_cores)(delayed(search_in_tile)(graph, tile, start, end) for tile in tiles[:10]))

append_features_to_file(features, "test_append.txt")



