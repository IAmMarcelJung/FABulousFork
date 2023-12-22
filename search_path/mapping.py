#!/bin/python
from search_path.node import NodeHeader

class Mapping:
    """Defines a mapping from UID to NodeHeader and back"""
    uid_to_node_header = {}
    node_header_to_uid = {}

    def add(self, node_header: NodeHeader, uid: int):
        """Add the name to the uid mapping.

        :param name str: The name to add to the mapping.
        :param uid int: The uid to add to the mapping
        :return: True if the mapping was added, else false.
        :rtype: bool
        """
        if node_header not in self.uid_to_node_header.values():
            self.uid_to_node_header[uid] = node_header
            self.node_header_to_uid[node_header] = uid
            return True
        else:
            return False



if __name__ == "__main__":
    pass
