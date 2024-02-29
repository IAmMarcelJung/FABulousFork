#!/bin/python3
import unittest

from modules.mapping import Mapping
from modules.tile import Tile
from modules.node import NodeHeader
from modules.graph import (
    get_nodes_from_file_for_tile,
    add_parents_and_children_for_tile,
)


class TestGraph(unittest.TestCase):
    def test_create_graph_from_file(self):
        """
        Test the creation of the graph from the pips file.
        """
        # graph = create_graph_from_file("tb_test/.FABulous/pips.txt")
        # Arrange
        file = "tests/test_files/pips.txt"
        tile = Tile(1, 1)
        mapping = Mapping()
        nodes = get_nodes_from_file_for_tile(file, tile, mapping)
        nodes = add_parents_and_children_for_tile(file, tile, nodes, mapping)

        node_0 = mapping.node_header_to_uid[NodeHeader("LA_O", tile)]
        node_1 = mapping.node_header_to_uid[NodeHeader("JW2BEG1", tile)]
        node_2 = mapping.node_header_to_uid[NodeHeader("JW2END1", tile)]
        node_3 = mapping.node_header_to_uid[NodeHeader("J_l_AB_BEG3", tile)]
        node_4 = mapping.node_header_to_uid[NodeHeader("J_l_AB_END3", tile)]
        node_5 = mapping.node_header_to_uid[NodeHeader("LA_I3", tile)]

        found_target = False
        # Act
        if node_1 in nodes[node_0].internal_children:
            if node_2 in nodes[node_1].internal_children:
                if node_3 in nodes[node_2].internal_children:
                    if node_4 in nodes[node_3].internal_children:
                        if node_5 in nodes[node_4].internal_children:
                            found_target = True
        final_node = mapping.uid_to_node_header[node_5]
        # Assert
        self.assertTrue(found_target)
        self.assertEqual("LA_I3", final_node.name)


if __name__ == "__main__":
    unittest.main()
