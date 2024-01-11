#!/bin/python
from search_path.node import NodeHeader

class Mapping:
    """Defines a mapping from UID to NodeHeader and back.

    :param Dict uid_to_node_header: The dicitonary mapping to map from uid to node header.
    :param Dict node_header_to_uid: The dicitonary mapping to map from node header to uid.
    """

    def __init__(self):
        self.uid_to_node_header = {}
        self.node_header_to_uid = {}

    def add(self, node_header: NodeHeader, uid: int):
        """Add the name to the uid mapping.

        :param name str: The name to add to the mapping.
        :param uid int: The uid to add to the mapping
        :return: True if the mapping was added, else false.
        :rtype: bool
        """
        if self.node_header_to_uid.setdefault(node_header) is None:
            self.node_header_to_uid[node_header] = uid
            self.uid_to_node_header[uid] = node_header
            return True
        else:
            return False


        """
        if node_header in self.uid_to_node_header.values():
            return False
        else:
            self.uid_to_node_header[uid] = node_header
            self.node_header_to_uid[node_header] = uid
            return True
            """

    def uid_path_to_node_header_path(self, uid_path: list):
        """
        Convert a path defined by UIDs to a path defined by node headers.

        :param uid_path List: The path defined by UIDs.
        :return The converted list containing node headers.
        :rtype: List
        """
        node_header_path = []
        for elem in uid_path:
            node_header_path.append(self.uid_to_node_header[elem])
        return node_header_path

    def node_header_path_to_uid(self, node_header_path: list):
        """
        Convert a path defined by UIDs to a path defined by node headers.

        :param node_header_path List: The path defined by node headers.
        :return The converted list containing UIDs.
        :rtype: List
        """
        uid_path = []
        for elem in node_header_path:
            uid_path.append(self.node_header_to_uid[elem])
        return uid_path


if __name__ == "__main__":
    pass
