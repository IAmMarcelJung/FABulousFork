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
    paths = {}

    while current_node != end_node_uid:
        for child in {*graph[current_node].internal_children, *graph[current_node].external_children}:
            if child not in visited:
                if current_node not in paths:
                    paths.update({current_node: [[current_node]]})
                for path in paths[current_node]:
                    if child not in paths:
                        paths.update({child: [[child] + path]})
                    else:
                        paths[child].append([child] + path)
                queue.append(child)
        if not queue:
            break
        current_node = queue.popleft()
        visited.add(current_node)

    start_node_uid = mapping.node_header_to_uid[start_node]
    matched = get_lists_where_first_and_last_element_matches(paths[end_node_uid], end_node_uid, start_node_uid)

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
