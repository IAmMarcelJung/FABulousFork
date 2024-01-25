#!/bin/python3

from typing import Dict, List, Set
from collections import deque

from search_path.node import NodeHeader
from search_path.mapping import Mapping
from search_path.utils import convert_paths
from search_path.tile import Tile

def print_nested_list(lst, mapping, depth=0):
    for element in lst:
        if isinstance(element, list):
            print_nested_list(element, mapping, depth + 1)
        else:
            print("  " * depth, mapping.uid_to_node_header[element])


def bfs(graph: Dict, start_node: NodeHeader, end_node: NodeHeader, mapping: Mapping, driven_nodes: Set, max_depth: int) -> List:
    """Do a breadth first search on the graph from the given start to end node.

    :param Dict graph: The graph in which to search the path.
    :param Node_Header start_node: The start node of the search.
    :param Node_Header end_node: The end node of the search.
    :param Mapping mapping: The mapping of UID to node header.
    :return: All paths with minimal length.
    :rtype: List
    """
    queue = deque()
    visited = set()
    current_node_uid = mapping.node_header_to_uid[start_node]
    end_node_uid = mapping.node_header_to_uid[end_node]
    visited.add(current_node_uid)
    paths = {}
    #print(f"Searching path from {start_node.tile}.{start_node.name} to {end_node.tile}.{end_node.name}")
    depth = 0
    #for node in driven_nodes:
    #    print(mapping.uid_to_node_header[node])
    while current_node_uid != end_node_uid:
        if depth > max_depth:
            return []
            break
        #paths.update({current_node_uid: [[current_node_uid]]})
        all_children = {*graph[current_node_uid].internal_children, *graph[current_node_uid].external_children}
        for child in all_children:
            if child not in visited and child not in driven_nodes:
            #if child not in visited:
                # create a path containing the current node
                if current_node_uid not in paths:
                    paths.update({current_node_uid: [[current_node_uid]]})
                for path in paths[current_node_uid]:
                    if child not in paths:
                        paths.update({child: [path + [child]]})
                    else:
                        paths[child].append(path + [child])
                    depth = len(path) + 1
                queue.append(child)
            '''
            else:
                if child in driven_nodes:
                    print(mapping.uid_to_node_header[child])
                    '''
        if not queue:
            return []
            break
        current_node_uid = queue.popleft()
        visited.add(current_node_uid)

    start_node_uid = mapping.node_header_to_uid[start_node]
    try:
        matched = get_lists_where_first_and_last_element_matches(paths[end_node_uid], start_node_uid, end_node_uid)
    except KeyError:
        #[print(mapping.uid_path_to_node_header_path(path)) for path in list(paths.values())[0]]
        #print(list(paths.values())[0])
        print_nested_list(list(paths.values()), mapping)
        print(mapping.uid_to_node_header[current_node_uid])
        print(mapping.uid_to_node_header[end_node_uid])
        raise


    return matched

def get_lists_where_first_and_last_element_matches(lists: List, start: str, end: str) -> List:
    """Get all lists where the first and the last element matches the given elements.

    :param List lists: The lists to be searched for the element.
    :param str start: The elem the list should start with.
    :param str end: The elem the list should end with.
    :return: All lists where the element was found as the first element of the given lists.
    :rtype: List
    """
    result_lists = []
    for tmplist in lists:
        if tmplist[0] == start and tmplist[-1] == end:
            result_lists.append(tmplist)
    return result_lists

def get_lists_where_last_element_matches(lists: List, elem: str) -> List:
    """Get all lists where the last element matches the given element.

    :param List lists: The lists to be searched for the element.
    :param str elem: The elem to be searched in the list.
    :return: All lists where the element was found as the last element of the given lists.
    :rtype: List
    """
    result_lists = []
    for tmplist in lists:
        if tmplist[-1] == elem:
            result_lists.append(tmplist)
    return result_lists

if __name__ == "__main__":
    pass
