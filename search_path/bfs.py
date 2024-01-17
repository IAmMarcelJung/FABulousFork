#!/bin/python3

from typing import Dict, List, Set
from collections import deque

from search_path.node import NodeHeader
from search_path.mapping import Mapping
from search_path.utils import convert_and_sort

def bfs(graph: Dict, start_node: NodeHeader, end_node: NodeHeader, mapping: Mapping) -> List:
    """Do a breadth first search on the graph from the given start to end node.

    :param Dict graph: The graph in which to search the path.
    :param Node_Header start_node: The start node of the search.
    :param Node_Header end_node: The end node of the search.
    :param Mapping mapping: The mapping of UID to node header.
    :return: All paths with minimal length
    :rtype: List
    """
    queue = deque()
    visited = set()
    current_node = mapping.node_header_to_uid[start_node]
    end_node_uid = mapping.node_header_to_uid[end_node]
    visited.add(current_node)
    paths = [[current_node]]
    append_paths(paths, current_node, graph, visited)

    while current_node != end_node_uid:
        for child in {*graph[current_node].internal_children, *graph[current_node].external_children}:
            if child not in visited:
                for path in graph[current_node].paths:
                    newpath = [child] + path
                    graph[child].paths.append(newpath)
                queue.append(child)
        if not queue:
            break
        current_node = queue.popleft()
        append_paths(paths, current_node, graph, visited)
        visited.add(current_node)

    """
    print(graph[end_node_uid].paths)
    #print(convert_and_sort(graph[end_node].paths, mapping))
    print(f"start: {start_node_uid}, end: {end_node_uid}.")
    print("!!!!!!!!!!!!!!!!")
    print(matched)
    print("!!!!!!!!!!!!!!!!")
    print(convert_and_sort(matched, mapping))
    """
    start_node_uid = mapping.node_header_to_uid[start_node]
    matched = get_lists_where_first_and_last_element_matches(graph[end_node_uid].paths, end_node_uid, start_node_uid)
    return matched
    #return get_lists_where_last_element_matches(paths, end_node_uid)

def get_lists_where_first_and_last_element_matches(lists: List, start: str, end: str) -> List:
    """Get all lists where the first and the last element matches the given elements.

    :param List lists: The lists to be searched for the element.
    :param str start: The elem the list shoud start with.
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

def append_paths(paths: List, current_node: NodeHeader, graph: Dict, visited: Set) -> None:
    """Append the paths by new found paths.

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

if __name__ == "__main__":
    pass
