#!/bin/python
import multiprocessing
from typing import Dict, Set

#import pdb; pdb.set_trace()

from search_path.tile import Tile, create_tile_from_string
from search_path.mapping import Mapping
from search_path.node import NodeHeader, Node

cpu_cores = max(multiprocessing.cpu_count(), 16)

def get_nodes_from_file_for_tile(pip_file: str, tile: Tile, mapping: Mapping) -> Set:
    """Extract all nodes for the given tile from a given pip file.

    :param str pip_file: The pip file where to extract the nodes from.
    :param Tile tile: The tile for which to extract the nodes.
    :param Mapping mapping: The mapping to to be used for the tile.
    :return The nodes extracted from the pip file for the given tile.
    :rtype Set
    """
    nodes = set()
    tile_str = tile.to_string()
    reached_current_tile = False
    uid = 0
    with open(pip_file) as f:
        for line in f:
            # Reached features of next tile, all features of current tile read
            if line.startswith('#') and reached_current_tile and tile_str not in line:
                break
            # Reached features of the current tile
            if reached_current_tile or (tile_str in line and line.startswith('#')):
                reached_current_tile = True
                if not line.startswith('#'):
                    # Do not use cost for now since its the same for all connections
                    source_tile, source_name, sink_tile, sink_name, cost, feature = line.split(',')
                    source_tile = create_tile_from_string(source_tile)
                    sink_tile = create_tile_from_string(sink_tile)
                    source_node = NodeHeader(source_name, source_tile)
                    sink_node = NodeHeader(sink_name, sink_tile)
                    if mapping.add(source_node, uid):
                        nodes.add(uid)
                        uid += 1
                    if mapping.add(sink_node, uid):
                        nodes.add(uid)
                        uid += 1
    return nodes

def get_nodes_from_file(pip_file: str, mapping: Mapping) -> Set:
    """Extract all nodes from a given pip file.

    :param str pip_file: The pip file where to extract the nodes from.
    :param Mapping mapping: The mapping to to be used for the tile.
    :return The nodes extracted from the pip file for the given tile.
    :rtype Set
    """
    nodes = set()
    uid = 0
    with open(pip_file) as f:
        for line in f:
            if not line.startswith('#'):
                # Do not use cost for now since its the same for all connections
                source_tile, source_name, sink_tile, sink_name, cost, feature = line.split(',')
                source_tile = create_tile_from_string(source_tile)
                sink_tile = create_tile_from_string(sink_tile)
                source_node = NodeHeader(source_name, source_tile)
                sink_node = NodeHeader(sink_name, sink_tile)
                if mapping.add(source_node, uid):
                    nodes.add(uid)
                    uid += 1
                if mapping.add(sink_node, uid):
                    nodes.add(uid)
                    uid += 1
    return nodes

def add_parents_and_children_for_tile(pip_file: str, tile: Tile, nodes_set: Set, mapping: Mapping) -> Dict:
    """Add the parent and the child nodes to all nodes.

    :param str pip_file: The pip file where to extract the child and parent nodes from.
    :param Tile tile: The tile for which to add the child and parent nodes to nodes.
    :param Set nodes_set: All previously created nodes.
    :param Mapping mapping: The mapping between tile string and UID.
    :return: All nodes associated with name, tile, parents and children, both internal and external.
    :rtype: Dict
    """
    nodes = {key: Node() for key in nodes_set}
    tile_str = tile.to_string()
    reached_current_tile = False
    with open(pip_file) as f:
        for line in f:
            # Reached features of next tile, all features of current tile read
            if line.startswith('#') and reached_current_tile and tile_str not in line:
                break
            # Reached features of the current tile
            if reached_current_tile or (tile_str in line and line.startswith('#')):
                reached_current_tile = True
                if not line.startswith('#'):
                    # Do not use cost for now since its the same for all connections
                    source_tile, source_name, sink_tile, sink_name, cost, feature = line.split(',')
                    source_tile = create_tile_from_string(source_tile)
                    sink_tile = create_tile_from_string(sink_tile)

                    source_node = NodeHeader(source_name, source_tile)
                    sink_node = NodeHeader(sink_name, sink_tile)

                    source_id = mapping.node_header_to_uid[source_node]
                    sink_id = mapping.node_header_to_uid[sink_node]

                    if source_tile == sink_tile:
                        nodes[sink_id].internal_parents.add(source_id)
                        nodes[source_id].internal_children.add(sink_id)
                    else:
                        nodes[sink_id].external_parents.add(source_id)
                        nodes[source_id].internal_children.add(sink_id)
    return nodes

def add_parents_and_children(pip_file: str, nodes_set: Set, mapping: Mapping) -> Dict:
    """Add the parent and the child nodes to all nodes.

    :param str pip_file: The pip file where to extract the child and parent nodes from.
    :param Set nodes_set: All previously created nodes.
    :param Mapping mapping: The mapping between tile string and UID.
    :return: The full graph.
    :rtype: Dict
    """
    graph = {key: Node() for key in nodes_set}
    with open(pip_file) as f:
        for line in f:
            if not line.startswith('#'):
                # Do not use cost for now since its the same for all connections
                source_tile, source_name, sink_tile, sink_name, cost, feature = line.split(',')
                source_tile = create_tile_from_string(source_tile)
                sink_tile = create_tile_from_string(sink_tile)

                source_node = NodeHeader(source_name, source_tile)
                sink_node = NodeHeader(sink_name, sink_tile)

                source_id = mapping.node_header_to_uid[source_node]
                sink_id = mapping.node_header_to_uid[sink_node]

                if source_tile == sink_tile:
                    graph[sink_id].internal_parents.add(source_id)
                    graph[source_id].internal_children.add(sink_id)
                else:
                    graph[sink_id].external_parents.add(source_id)
                    graph[source_id].internal_children.add(sink_id)

    return graph

def create_graph(pip_file: str, mapping: Mapping) -> Dict:
    """
    Create the connection graph.

    :param str pip_file: The file containing the pips.
    :param Mapping mapping: The mapping between the UID and the node header.
    """
    nodes = get_nodes_from_file(pip_file, mapping)
    graph = add_parents_and_children(pip_file, nodes, mapping)
    return graph

if __name__ == "__main__":
    pass
