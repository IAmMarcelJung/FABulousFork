#!/bin/python
import re
import multiprocessing
import pprint as pp
from more_itertools import peekable
from collections import deque
from typing import *
from dataclasses import dataclass
from tqdm import tqdm
from joblib import Parallel, delayed

#import pdb; pdb.set_trace()

from search_path.tile import *
from search_path.utils import *
from search_path.mapping import *
from search_path.node import *

cpu_cores = max(multiprocessing.cpu_count(), 16)

#uid_to_node_header_mapping = {}
#node_header_to_uid_mapping = {}
nodes = set()

'''@dataclass(frozen=True)
class NodeHeader():
    """Defines a node header with the node name and the tile of the node."""
    name: str
    tile: Tile

class Node:
    """Defines a node.
    Like a node header, a node has a name and is associated to a tile.
    It also has both internal and external parent and child nodes.

    :param internal_parents: The parent nodes located on the same tile.
    :param internal_children: The child nodes located on the same tile.
    :param external_parents: The child nodes located on another tile.
    :param external_children: The parent nodes located on another tile.
    """
    #def __init__(self, header: NodeHeader, uid: int):
    def __init__(self, uid: int):
        self.internal_parents = set()
        self.internal_children = set()
        self.external_parents = set()
        self.external_children = set()
        #self.tile = header.tile
        #self.name = header.name
        #self.uid = uid
'''
'''
def add_to_uid_mapping(node_header: NodeHeader, uid: int, mapping: Dict, mapping_reverse: Dict) -> bool:
    """Add the name to the uid mapping.

    :param name str: The name to add to the mapping.
    :param uid int: The uid to add to the mapping
    :return: True if the mapping was added, else false.
    :rtype: bool
    """
    if node_header not in uid_to_node_header_mapping.values():
        #uid_to_node_header_mapping[uid] = node_header
        #node_header_to_uid_mapping[node_header] = uid
        mapping[uid] = node_header
        mapping_reverse[node_header] = uid
        return True
    else:
        return False

'''

def str_to_tile(tile_str: str) -> Tile:
    """Create a tile from a string.

    :param str tile_str: The tile as a string to be converted.
    :return: The tile string converted to a Tile.
    :rtype: Tile
    """
    parts = tile_str.split('Y')
    x = parts[0].strip('X')
    y = parts[1].strip('Y')
    return Tile(int(x), int(y))

def get_nodes_from_file_for_tile(pip_file: str, tile: Tile, mapping: Mapping) -> Set:
    """Extract all nodes for the given tile from a given pip file

    :param str pip_file: The pip file where to extract the nodes from.
    :param Tile tile: The tile for which to extract the nodes.
    :param Mapping mapping: The mapping to to be used for the tile.
    :return The nodes extracted from the pip file for the given tile.
    :rtype Set
    """
    #nodes = set()
    tile_str = tile.to_string()
    next_tile = Tile(tile.x + 1, tile.y)
    next_tile_str = next_tile.to_string()
    is_current_tile = False
    uid = 0
    with open(pip_file) as f:
        for line in f:
            # Reached features of next tile, all features of current tile read
            if line.startswith('#') and next_tile_str in line:
                break
            # Reached features of the current tile
            if is_current_tile or (tile_str in line and line.startswith('#')):
                is_current_tile = True
                if not line.startswith('#'):
                    # Do not use cost for now since its the same for all connections
                    source_tile, source_name, sink_tile, sink_name, cost, feature = line.split(',')
                    source_tile = str_to_tile(source_tile)
                    sink_tile = str_to_tile(sink_tile)
                    source_node = NodeHeader(source_name, source_tile)
                    sink_node = NodeHeader(sink_name, sink_tile)
                    #if add_to_uid_mapping(source_node, uid):
                    if mapping.add(source_node, uid):
                        nodes.add(uid)
                        uid += 1
                    #if add_to_uid_mapping(sink_node, uid):
                    if mapping.add(sink_node, uid):
                        nodes.add(uid)
                        uid += 1
                    #nodes.add(source_node)
                    #nodes.add(sink_node)
    return nodes

def add_parents_and_children(pip_file: str, tile: Tile, nodes_set: Set, mapping: Mapping) -> Dict:
    """Add the parent and the child nodes to all nodes.

    :param str pip_file: The pip file where to extract the child and parent nodes from.
    :param Tile tile: The tile for which to add the child and parent nodes to nodes.
    :param Set nodes_set: All previously created nodes.
    :param Mapping mapping: The mapping between tile string and UID.
    :return All nodes associated with name, tile, parents and children, both internal and external.
    """
    nodes = {key: Node() for key in nodes_set}
    tile_str = tile.to_string()
    next_tile = Tile(tile.x + 1, tile.y)
    next_tile_str = next_tile.to_string()
    is_current_tile = False
    uid = 0
    if tile == Tile(1, 1):
        pass
        #print(node_header_to_uid_mapping)
    with open(pip_file) as f:
        for line in f:
            # Reached features of next tile, all features of current tile read
            if line.startswith('#') and next_tile_str in line:
                break
            # Reached features of the current tile
            if is_current_tile or (tile_str in line and line.startswith('#')):
                is_current_tile = True
                if not line.startswith('#'):
                    # Do not use cost for now since its the same for all connections
                    source_tile, source_name, sink_tile, sink_name, cost, feature = line.split(',')
                    source_tile = str_to_tile(source_tile)
                    sink_tile = str_to_tile(sink_tile)

                    source_node = NodeHeader(source_name, source_tile)
                    sink_node = NodeHeader(sink_name, sink_tile)

                    #source_node = NodeHeader(source_id, source_tile)
                    #sink_node = NodeHeader(sink_id, sink_tile)

                    source_id = mapping.node_header_to_uid[source_node]
                    sink_id = mapping.node_header_to_uid[sink_node]

                    if source_tile == sink_tile:
                        #nodes[sink_node].internal_parents.add(source_node)
                        #nodes[source_node].internal_children.add(sink_node)
                        nodes[sink_id].internal_parents.add(source_id)
                        nodes[source_id].internal_children.add(sink_id)
                    else:
                        nodes[sink_id].external_parents.add(source_id)
                        nodes[source_id].internal_children.add(sink_id)
                        #nodes[sink_node].external_parents.add(source_node)
                        #nodes[source_node].external_children.add(sink_node)
                    #nodes[sink_node].uid = sink_id
                    #nodes[source_node].uid = source_id
                    #nodes[sink_node].name = sink
                    #nodes[source_node].name = source
                    #nodes[sink_node].tile = sink_tile

    return nodes

def append_paths(paths: List, current_node: NodeHeader, graph: Dict, visited: Set) -> None:
    """Append the paths by new found paths

    :param List paths: The previously found paths.
    :param Node_Header current: The node for which the children should be appended to the paths.
    :param Dict graph: The graph containing all nodes.
    :param Set visited: All previously visited nodes.
    """
    new_paths = []
    for path in paths:
        if current_node in path:
            for child in {*graph[current_node].internal_children, *graph[current_node].external_children}:
                if child not in visited and child not in path:
                    new_list = path.copy()
                    new_list.append(child)
                    new_paths.append(new_list)
    paths += new_paths

def get_lists_where_last_element_matches(lists: List, elem: str) -> List:
    """Get all lists where the last element matches the given element.

    :param List lists: The lists to be searched for the element.
    :param str elem: The elem to be searched in the list.
    :return All lists where the element was found as the last element of the given lists.
    :rtype List
    """
    result_lists = []
    for tmplist in lists:
        if tmplist[-1] == elem:
            result_lists.append(tmplist)
    return result_lists


def bfs(graph: Dict, start_node: NodeHeader, end_node: NodeHeader, mapping: Mapping) -> List:
    """Do a breadth first search on the graph from the given start to end node.

    :param Dict graph: The graph in which to search the path.
    :param Node_Header start_node: The start node of the search.
    :param Node_Header end_node: The end node of the search.
    :param Mapping mapping: The mapping of UID to node header.
    :return All paths with minimal length
    :rtype List
    """
    queue = deque()
    visited = set()
    current_node = mapping.node_header_to_uid[start_node]
    end_node = mapping.node_header_to_uid[end_node]
    visited.add(current_node)
    paths = [[current_node]]
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

def create_features(path: List) -> List:
    """ Create the FASM features from the given path.

    :param List path: The path for which to create the FASM features.
    :return All features created from the path.
    :rtype List
    """
    feature_list = []
    path = peekable(path)
    for elem in path:
        if path:
            current_tile = elem
            tile = elem.tile
            tile_str = tile.to_string()
            source = elem.name

            next_elem = path.peek()
            sink = next_elem.name

            feature = f'{tile_str}.{source}.{sink}'
            feature_list.append(feature)
            if re.search('L[A-Z]_[1-5]', sink):
                print(sink)

    return feature_list

def append_features_to_file(features: List, file: str) -> None:
    """Append the features to an existing file.

    :param List features: The features to append to the file.
    :param str file: The file where to append the features to.
    """
    found_start = False
    with open(file, 'r+') as f:
        for line in iter(f.readline, ''):
            if '#additional features' in line:
            #if line.startswith('#additional features'):
                f.seek(0, 1)
                f.truncate()
                found_start = True
                break

        if not found_start:
            f.write('#additional features\n')
        for feature in features:
            f.write(feature + '\n')

def create_graph_for_all_tiles_of_type(fabric_file: str, pip_file: str, tile_type: Tile.Types, mapping: Mapping) -> Dict:
    """
    Create the connection graph for all tiles of the specified type.
    :param str fabric_file: The file containing the fabric definition in csv format.
    :param str pip_file: The file containing the pips.
    :param Tile.Types tile_type: The tile type to create the graph for.
    :return The graph created for all tiles of the type.
    :rtype Dict
    """
    tiles = get_tiles_for_fabric(fabric_file)
    tiles = get_all_locations_of_tile_type(tile_type, tiles)
    #tiles = get_all_locations_of_tiles(tiles)
    graph = {}
    '''for tile in tqdm(tiles):
        tile_graph = create_graph_for_tile(pip_file, tile)
        graph = graph | tile_graph

'''
    print(f"Creating graph for all tiles of type {tile_type}:")
    tile_graphs= list(
        tqdm(
            Parallel(return_as="generator", n_jobs=cpu_cores)(
                delayed(create_graph_for_tile)(pip_file, tile, mapping) for tile in tiles
            ),
            total=len(tiles),
        )
    )

    mappings = Mapping()
    for tile_graph in tile_graphs:
        value: Node
        graph = graph | tile_graph[0]
        print(tile_graph[1].uid_to_node_header)
        print(tile_graph[1].node_header_to_uid)
        mappings.uid_to_node_header = mappings.uid_to_node_header | tile_graph[1].uid_to_node_header
        mappings.node_header_to_uid = mappings.node_header_to_uid | tile_graph[1].node_header_to_uid
    return graph, mappings



def create_graph_for_tile(pip_file: str, tile: Tile, mapping: Mapping) -> Dict:
    """
    Create the connection graph for a given tile.

    :param str pip_file: The file containing the pips.
    :param Tile tile: The tile to create the graph for.
    """
    nodes = get_nodes_from_file_for_tile(pip_file, tile, mapping)
    graph = add_parents_and_children(pip_file, tile, nodes, mapping)
    return graph, mapping

if __name__ == "__main__":
    pass
