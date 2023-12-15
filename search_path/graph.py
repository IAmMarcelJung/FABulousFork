#!/bin/python
from collections import deque
from typing import *
#import pdb; pdb.set_trace()
from dataclasses import dataclass

@dataclass(frozen=True)
class Tile:
    '''def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        '''
    x: int
    y: int

@dataclass(frozen=True)
class Node_Header:
    '''def __init__(self, name: str, tile: Tile):
        self.tile = tile
        self.name = name
        '''
    name: str
    tile: Tile

class Node:
    def __init__(self, header: Node_Header):
        self.internal_parents = set()
        self.internal_children = set()
        self.external_parents = set()
        self.external_children = set()
        self.tile = header.tile
        self.name = header.name

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
                    source_tile, source, sink_tile, sink, dnc, feature = line.split(',')
                    source_tile = str_to_tile(source_tile)
                    sink_tile = str_to_tile(sink_tile)
                    source_node = Node_Header(source, source_tile)
                    sink_node = Node_Header(sink, sink_tile)
                    nodes.add(source_node)
                    nodes.add(sink_node)
    return nodes

def add_parents_and_children(pip_file: str, tile: Tile, nodes_set: Set):
    nodes = {key: Node(key) for key in nodes_set}
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
                    source_tile, source, sink_tile, sink, dnc, feature = line.split(',')
                    source_tile = str_to_tile(source_tile)
                    sink_tile = str_to_tile(sink_tile)
                    source_node = Node_Header(source, source_tile)
                    sink_node = Node_Header(sink, sink_tile)
                    if source_tile == sink_tile:
                        nodes[sink_node].internal_parents.add(source_node)
                        nodes[source_node].internal_children.add(sink_node)
                    else:
                        nodes[sink_node].external_parents.add(source_node)
                        nodes[source_node].external_children.add(sink_node)
                    nodes[sink_node].name = sink
                    nodes[sink_node].tile = sink_tile
                    nodes[source_node].name = source
                    nodes[source_node].tile = source_tile
    return nodes

def append_paths(paths: List, node: Node_Header, graph: Dict, visited: Set):
    new_paths = []
    for path in paths:
        if node in path:
            for child in {*graph[node].internal_children, *graph[node].external_children}:
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


def bfs(graph: Dict, start_node: Node_Header, end_node: Node_Header):
    queue = deque()
    visited = set()
    current_node = start_node
    visited.add(current_node)
    paths = [[start_node]]
    append_paths(paths, current_node, graph, visited)

    while current_node != end_node:
        for child in {*graph[current_node].internal_children, *graph[current_node].external_children}:
            if child not in visited:
                queue.append(child)
        if not queue:
            break
        current_node = queue.popleft()
        append_paths(paths, current_node, graph, visited)
        visited.add(current_node)

    return get_lists_where_last_element_matches(paths, end_node)

def create_features(path: List):
    feature_list = []
    for i in range(len(path[:-1])):
        tile = path[i].tile
        tile_str = tile_to_str(tile)
        source = path[i].name
        sink = path[i+1].name
        feature = f"{tile_str}.{source}.{sink}"
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
