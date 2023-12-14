#!/bin/python
import heapq
from collections import deque
from typing import *
#import pdb; pdb.set_trace()

class Node:
    def __init__(self, internal_parents: Set, internal_children: Set, external_parents: Set, external_children: Set):
        self.internal_parents = internal_parents
        self.internal_children = internal_children
        self.external_parents = external_parents
        self.external_children = external_children
        self.tile = Tile(0,0)
        self.name = ""

class Tile:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

def create_graph_from_file(pip_file):
    graph = PipeGraph()
    with open(pip_file) as f:
        for line in f:
            if line.startswith('#'):
                continue
            # Split the line into its components
            source_tile, sink, destination_tile, source, dnc, feature = line.split(',')
            # Create a pipe node and add it to the graph
            pipe_node = PipeNode(source_tile, source, destination_tile, sink, _)
            graph.add_node(pipe_node)
    return graph

def tile_to_str(tile: Tile):
    return f"X{tile.x}Y{tile.y}"

def str_to_tile(tile_str: str):
    parts = tile_str.split('Y')
    x = parts[0].strip('X')
    y = parts[1].strip('Y')
    return Tile(int(x), int(y))


def get_nodes_from_file_for_tile(pip_file: str, tile: Tile):
    nodes = set()
    tile_str = tile_to_str(tile)
    next_tile = Tile(tile.x + 1, tile.y)
    next_tile_str = tile_to_str(next_tile)
    is_current_tile = False
    with open(pip_file) as f:
        for line in f:
            # Reached features of next tile, all features of current tile read
            if line.startswith('#') and next_tile_str in line:
                break
            # Reached features of the current tile
            if is_current_tile or (tile_str in line and line.startswith("#")):
                is_current_tile = True
                if not line.startswith("#"):
                    source_tile, sink, destination_tile, source, dnc, feature = line.split(',')
                    nodes.add(sink)
                    nodes.add(source)
    return nodes

def add_parents_and_children(pip_file: str, tile: Tile, nodes_set: Set):
    nodes = { key: Node(set(), set(), set(), set()) for key in nodes_set}
    tile_str = tile_to_str(tile)
    next_tile = Tile(tile.x + 1, tile.y)
    next_tile_str = tile_to_str(next_tile)
    is_current_tile = False
    with open(pip_file) as f:
        for line in f:
            # Reached features of next tile, all features of current tile read
            if line.startswith('#') and next_tile_str in line:
                break
            # Reached features of the current tile
            if is_current_tile or (tile_str in line and line.startswith("#")):
                is_current_tile = True
                if not line.startswith("#"):
                    source_tile, source, destination_tile, sink, dnc, feature = line.split(',')
                    if source_tile == destination_tile:
                        nodes[sink].internal_parents.add(source)
                        nodes[source].internal_children.add(sink)
                    else:
                        nodes[sink].external_parents.add(source)
                        nodes[source].external_children.add(sink)
                    nodes[sink].name = sink
                    nodes[sink].tile = destination_tile
                    nodes[source].name = source
    return nodes

def append_paths(paths: List, current_node: str, graph: Dict, visited: Set):
    new_paths = []
    for path in paths:
        if current_node in path:
            for child in graph[current_node].internal_children:
                if child not in visited and child not in path:
                    new_list = path.copy()
                    new_list.append(child)
                    new_paths.append(new_list)
    paths += new_paths

def get_lists_where_last_element_matches(lists: List, elem: str):
    result_lists = []
    for tmplist in lists:
        if tmplist[-1] == elem:
            result_lists.append(tmplist)
    return result_lists


def bfs(graph: Dict, start_node_name: str, end_node_name: str):
    queue = deque()
    visited = set()
    current_node = start_node_name
    visited.add(current_node)
    paths = [[start_node_name]]
    append_paths(paths, current_node, graph, visited)

    while current_node != end_node_name:
        if graph[current_node].internal_children:
            for child in graph[current_node].internal_children:
                if child not in visited:
                    queue.append(child)
        if not queue:
            break
        current_node = queue.popleft()
        append_paths(paths, current_node, graph, visited)
        visited.add(current_node)

    return get_lists_where_last_element_matches(paths, end_node_name)

def create_features(path: List):
    feature_list = []
    for i in range(len(path[:-1])):
        feature = f"{path[i]}.{path[i+1]}"
        feature_list.append(feature)
    return feature_list

def append_features_to_file(features: List, file: str):
    with open(file, 'r+') as f:
        for line in f:
            if line.startswith("#additional features"):
                f.truncate()
                break

        f.write("# additional features\n")
        for feature in features:
            f.write(feature + '\n')

if __name__ == "__main__":
    pass
