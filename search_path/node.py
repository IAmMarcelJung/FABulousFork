#!/bin/python
from dataclasses import dataclass
from search_path.tile import Tile

@dataclass(frozen=True)
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
    def __init__(self):
        self.internal_parents = set()
        self.internal_children = set()
        self.external_parents = set()
        self.external_children = set()

if __name__ == "__main__":
    pass
