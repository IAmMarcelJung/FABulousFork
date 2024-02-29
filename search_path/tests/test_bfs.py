#!/bin/python3
import os
import unittest
import time

# import cProfile
# from unittest.mock import Mock
# from unittest.mock import patch
from context import modules
from modules.utils import get_tiles_for_fabric, get_all_locations_of_tile_type
from modules.mapping import Mapping
from modules.tile import Tile
from modules.bfs import bfs, get_lists_where_last_element_matches
from modules.node import NodeHeader
from modules.fasm_features import (
    create_features_with_gnd_and_init,
    append_features_to_file,
)
from modules.graph import (
    create_graph,
)

test_dir = os.path.join(os.path.dirname(__file__), "test_files")
test_file = os.path.join(test_dir, "test_features.txt")
fabric_file = os.path.join(test_dir, "fabric.csv")
# fabric_file = "tests/test_files/fabric.csv"
default_max_depth = 15


class TestBfs(unittest.TestCase):
    graph = {}
    # pip_file = "tests/test_files/pips.txt"
    pip_file = os.path.join(test_dir, "pips.txt")
    mapping = Mapping()
    graph = create_graph(pip_file, mapping)

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.6f" % (self.id(), t))

    """
    @patch("search_path.bfs.SearchPath.beg_to_end")
    def test_end_to_beg(self, mock_beg_to_end):
        mock_beg_to_end.return_value = False

        retval = self.sp.end_to_beg("J_l_AB_END3", "LA_I3", self.best, self.current_path)
        self.assertTrue(retval, "Expected True, got False")
        self.assertTrue(self.best.cost == 1, f"Expected {1} got {self.best.cost}")

    @patch("search_path.bfs.SearchPath.end_to_beg")
    def test_beg_to_end(self, mock_end_to_beg):
        mock_end_to_beg.return_value = False

        retval = self.sp.beg_to_end("J_l_AB_BEG3" ,"J_l_AB_END3", self.best, self.current_path)
        self.assertTrue(retval, "Expected True, got False")
        self.assertTrue(self.best.cost == 1, f"Expected {1} got {self.best.cost}")

    """

    def test_bfs_X1Y1_output_to_input(self):
        """
        Test the search of a path from an output to an input in X1Y1.
        """
        # Arrange
        tile = Tile(1, 1)

        start_node = NodeHeader("LA_O", tile)
        end_node = NodeHeader("LA_I3", tile)
        target_path = [
            NodeHeader(name="LA_O", tile=Tile(x=1, y=1)),
            NodeHeader(name="JW2BEG1", tile=Tile(x=1, y=1)),
            NodeHeader(name="JW2END1", tile=Tile(x=1, y=1)),
            NodeHeader(name="J_l_AB_BEG3", tile=Tile(x=1, y=1)),
            NodeHeader(name="J_l_AB_END3", tile=Tile(x=1, y=1)),
            NodeHeader(name="LA_I3", tile=Tile(x=1, y=1)),
        ]
        target_path = self.mapping.node_header_path_to_uid(target_path)

        # Act
        paths = bfs(
            self.graph, start_node, end_node, self.mapping, set(), default_max_depth
        )

        print(f"expected paths: {paths}")
        print(f"Target path: {target_path}")

        # Assert
        self.assertTrue(target_path in paths, "Could not find path from LA_O to LA_I3")

    def test_bfs_X1Y1_turnaround(self):
        """
        Test the search of a turnaround in X1Y1.
        """
        # Arrange
        tile = Tile(1, 1)

        start_node = NodeHeader("E6END0", tile)
        end_tile = Tile(0, 1)
        end_node = NodeHeader("W2MID3", end_tile)
        target_path = [
            NodeHeader("E6END0", tile),
            NodeHeader("JW2BEG3", tile),
            NodeHeader("JW2END3", tile),
            NodeHeader("W2BEG3", tile),
            NodeHeader("W2MID3", end_tile),
        ]
        target_path = self.mapping.node_header_path_to_uid(target_path)

        # Act
        paths = bfs(
            self.graph, start_node, end_node, self.mapping, set(), default_max_depth
        )

        # Assert
        self.assertTrue(
            target_path in paths, "Could not find path from E6END0 to W2MID3"
        )

    def test_bfs_X1Y1_partial_path(self):
        """
        Test the search of a partial path in X1Y1.
        """
        # Arrange
        tile = Tile(1, 1)

        start_node = NodeHeader("E1END0", tile)
        end_node = NodeHeader("LA_I0", tile)
        target_path = [
            NodeHeader("E1END0", tile),
            NodeHeader("JN2BEG1", tile),
            NodeHeader("JN2END1", tile),
            NodeHeader("J_l_AB_BEG0", tile),
            NodeHeader("J_l_AB_END0", tile),
            NodeHeader("LA_I0", tile),
        ]
        target_path = self.mapping.node_header_path_to_uid(target_path)

        # Act
        paths = bfs(
            self.graph, start_node, end_node, self.mapping, set(), default_max_depth
        )

        # Assert
        self.assertTrue(
            target_path in paths, "Could not find path from E1END0 to LA_I0"
        )

    def test_bfs_X0Y1_partial_path(self):
        """
        Test the search of a partial path in X0Y1.
        """
        # Arrange
        tile = Tile(0, 1)

        start_node = NodeHeader("A_O", tile)
        end_node = NodeHeader("E1BEG0", tile)
        target_path = [start_node, NodeHeader("E1BEG0", tile)]
        target_path = self.mapping.node_header_path_to_uid(target_path)

        # Act
        paths = bfs(
            self.graph, start_node, end_node, self.mapping, set(), default_max_depth
        )

        # Assert
        self.assertTrue(
            target_path in paths, "Could not find path from X0Y1.A_O to X0Y1.E1BEG0"
        )

    def test_bfs_io_output_to_lut_input(self):
        """
        Test the search of a partial path in X0Y1.
        """
        # Arrange
        tile = Tile(0, 1)

        end_tile = Tile(1, 1)
        start_node = NodeHeader("A_O", tile)
        end_node = NodeHeader("LA_I0", end_tile)
        target_path = [
            start_node,
            NodeHeader("E1BEG0", tile),
            NodeHeader("E1END0", end_tile),
            NodeHeader("JN2BEG1", end_tile),
            NodeHeader("JN2END1", end_tile),
            NodeHeader("J_l_AB_BEG0", end_tile),
            NodeHeader("J_l_AB_END0", end_tile),
            NodeHeader("LA_I0", end_tile),
        ]
        target_path = self.mapping.node_header_path_to_uid(target_path)

        # Act
        paths = bfs(
            self.graph, start_node, end_node, self.mapping, set(), default_max_depth
        )

        # Assert
        print(self.mapping.uid_path_to_node_header_path(target_path))
        self.assertTrue(
            target_path in paths, "Could not find path from X0Y1.A_O to X1Y1.LA_I0"
        )

    def test_get_lists_where_last_element_matches(self):
        """
        Test the function which gets the lists where the last element matches a given element.
        """
        # Arrange
        lists = [["1"], ["1", "2"], ["1", "2", "3"], ["1", "2", "3", "4"]]

        # Act
        result = get_lists_where_last_element_matches(lists, "4")

        # Assert
        self.assertCountEqual(result, [["1", "2", "3", "4"]])

    def test_create_features(self):
        """
        Test the creation of features from a given path.
        """
        # Arrange
        target_path = [
            "LA_O",
            "JW2BEG1",
            "JW2END1",
            "J_l_AB_BEG3",
            "J_l_AB_END3",
            "LA_I3",
        ]
        target_path = [
            NodeHeader(name="LA_O", tile=Tile(x=1, y=1)),
            NodeHeader(name="JW2BEG1", tile=Tile(x=1, y=1)),
            NodeHeader(name="JW2END1", tile=Tile(x=1, y=1)),
            NodeHeader(name="J_l_AB_BEG3", tile=Tile(x=1, y=1)),
            NodeHeader(name="J_l_AB_END3", tile=Tile(x=1, y=1)),
            NodeHeader(name="LA_I3", tile=Tile(x=1, y=1)),
        ]

        # No IO tile, do not add GND
        target_features = [
            "X1Y1.LA_O.JW2BEG1",
            "X1Y1.JW2BEG1.JW2END1",
            "X1Y1.JW2END1.J_l_AB_BEG3",
            "X1Y1.J_l_AB_BEG3.J_l_AB_END3",
            "X1Y1.J_l_AB_END3.LA_I3",
            "X1Y1.A.INIT[0]",
            "X1Y1.A.FF",
        ]
        used_tiles = set()
        # Act
        features = create_features_with_gnd_and_init(target_path, used_tiles)
        # Assert
        self.assertCountEqual(target_features, features)

    def test_append_features_to_file(self):
        """
        Test the appending of features to a file without overriding features created by FABulous.
        """
        # Arrange
        features = [
            "X1Y1.LA_O.JW2BEG1",
            "X1Y1.JW2BEG1.JW2END1",
            "X1Y1.JW2END1.J_l_AB_BEG3",
            "X1Y1.J_l_AB_BEG3.J_l_AB_END3",
            "X1Y1.J_l_AB_END3.LA_I3",
        ]
        lines = [
            "#Path for X1Y1:",
            "X1Y1.LA_O.JW2BEG1",
            "X1Y1.JW2BEG1.JW2END1",
            "X1Y1.JW2END1.J_l_AB_BEG3",
            "X1Y1.J_l_AB_BEG3.J_l_AB_END3",
            "X1Y1.J_l_AB_END3.LA_I3",
        ]
        self.assertFalse(os.path.exists(test_file))
        open(test_file, "w").close()
        self.assertTrue(os.path.exists(test_file))
        start_found = False

        # Act
        append_features_to_file(features, test_file)

        # Assert
        with open(test_file, "r") as f:
            index = 0
            for line in f:
                if line.startswith("\n"):
                    continue
                if start_found:
                    self.assertEqual(line.rstrip("\n"), lines[index])
                    index += 1
                if line.startswith("#additional features"):
                    if start_found:
                        self.assertFalse(
                            start_found,
                            "Found multiple lines containing '#additional features'",
                        )
                    start_found = True
        self.assertTrue(start_found)

        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

    def test_get_tiles_for_fabric_return_correct_dict(self):
        """
        Test the reading of the file types in a fabric.
        """
        # Arrange

        # Act
        tiles = get_tiles_for_fabric(fabric_file)

        # Assert
        self.assertEqual(tiles[Tile(0, 0)], "NULL")
        self.assertEqual(tiles[Tile(9, 0)], "N_term_RAM_IO")
        self.assertEqual(tiles[Tile(0, 15)], "NULL")
        self.assertEqual(tiles[Tile(9, 15)], "S_term_RAM_IO")
        self.assertEqual(tiles[Tile(0, 1)], "W_IO")
        self.assertEqual(tiles[Tile(1, 1)], "LUT4AB")

    def test_get_all_locations_of_tile_type_LUT4AB_return_full_list(self):
        """
        Test the reading of the location of all LUT4AB tiles.
        """
        # Arrange
        tile_type = Tile.Types.LUT4AB
        locations_truth = [
            Tile(1, 1),
            Tile(2, 1),
            Tile(4, 1),
            Tile(5, 1),
            Tile(7, 1),
            Tile(8, 1),
            Tile(1, 2),
            Tile(2, 2),
            Tile(4, 2),
            Tile(5, 2),
            Tile(7, 2),
            Tile(8, 2),
            Tile(1, 3),
            Tile(2, 3),
            Tile(4, 3),
            Tile(5, 3),
            Tile(7, 3),
            Tile(8, 3),
            Tile(1, 4),
            Tile(2, 4),
            Tile(4, 4),
            Tile(5, 4),
            Tile(7, 4),
            Tile(8, 4),
            Tile(1, 5),
            Tile(2, 5),
            Tile(4, 5),
            Tile(5, 5),
            Tile(7, 5),
            Tile(8, 5),
            Tile(1, 6),
            Tile(2, 6),
            Tile(4, 6),
            Tile(5, 6),
            Tile(7, 6),
            Tile(8, 6),
            Tile(1, 7),
            Tile(2, 7),
            Tile(4, 7),
            Tile(5, 7),
            Tile(7, 7),
            Tile(8, 7),
            Tile(1, 8),
            Tile(2, 8),
            Tile(4, 8),
            Tile(5, 8),
            Tile(7, 8),
            Tile(8, 8),
            Tile(1, 9),
            Tile(2, 9),
            Tile(4, 9),
            Tile(5, 9),
            Tile(7, 9),
            Tile(8, 9),
            Tile(1, 10),
            Tile(2, 10),
            Tile(4, 10),
            Tile(5, 10),
            Tile(7, 10),
            Tile(8, 10),
            Tile(1, 11),
            Tile(2, 11),
            Tile(4, 11),
            Tile(5, 11),
            Tile(7, 11),
            Tile(8, 11),
            Tile(1, 12),
            Tile(2, 12),
            Tile(4, 12),
            Tile(5, 12),
            Tile(7, 12),
            Tile(8, 12),
            Tile(1, 13),
            Tile(2, 13),
            Tile(4, 13),
            Tile(5, 13),
            Tile(7, 13),
            Tile(8, 13),
            Tile(1, 14),
            Tile(2, 14),
            Tile(4, 14),
            Tile(5, 14),
            Tile(7, 14),
            Tile(8, 14),
        ]
        tiles = get_tiles_for_fabric(fabric_file)

        # Act
        locations = get_all_locations_of_tile_type(tile_type, tiles)

        # Assert
        self.assertCountEqual(locations_truth, locations)

    def test_get_all_locations_of_tile_type_NULL_return_full_list(self):
        """
        Test the reading of the location of all NULL tiles.
        """
        # Arrange
        tile_type = Tile.Types.NULL
        locations_truth = [Tile(0, 0), Tile(0, 15)]
        tiles = get_tiles_for_fabric(fabric_file)

        # Act
        locations = get_all_locations_of_tile_type(tile_type, tiles)

        # Assert
        self.assertCountEqual(locations_truth, locations)

    def test_uid_path_to_node_header_path(self):
        """
        Test the conversion of a path defined by UIDs to a path defined by node headers.
        """
        # Arrange
        tile = Tile(0, 0)
        uid_path = [0, 1, 2, 3]
        node_header_path = [
            NodeHeader("A", tile),
            NodeHeader("B", tile),
            NodeHeader("C", tile),
            NodeHeader("D", tile),
        ]
        for i in range(min(len(node_header_path), len(uid_path))):
            self.mapping.add(node_header_path[i], uid_path[i])

        # Act
        result = self.mapping.uid_path_to_node_header_path(uid_path)

        # Assert
        self.assertCountEqual(result, node_header_path)

    def test_node_header_path_to_uid(self):
        """
        Test the conversion of a path defined by node headers to a path defined by UIDs.
        """
        # Arrange
        tile = Tile(0, 0)
        uid_path = [0, 1, 2, 3]
        node_header_path = [
            NodeHeader("A", tile),
            NodeHeader("B", tile),
            NodeHeader("C", tile),
            NodeHeader("D", tile),
        ]
        for i in range(min(len(node_header_path), len(uid_path))):
            self.mapping.add(node_header_path[i], uid_path[i])

        # Act
        result = self.mapping.uid_path_to_node_header_path(uid_path)

        # Assert
        self.assertCountEqual(result, node_header_path)


'''
class TestAppendPaths(unittest.TestCase):

    def test_append_paths(self):
        """
        Test the appending of nodes to a path.
        """
        #Arrange
        tile = Tile(1,1)
        mapping = Mapping()
        target_paths = [[NodeHeader(name="LA_O", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JS2BEG1", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JE2BEG5", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JW2BEG5", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JE2BEG6", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="S4BEG0", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JS2BEG2", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="SS4BEG1", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JW2BEG3", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JW2BEG6", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JW2BEG4", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JS2BEG4", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JN2BEG4", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="E6BEG1", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JN2BEG1", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JN2BEG6", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JW2BEG2", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JE2BEG4", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JN2BEG7", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JS2BEG6", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JE2BEG2", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JS2BEG3", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JS2BEG7", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="NN4BEG1", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JN2BEG3", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="W6BEG1", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JE2BEG3", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JE2BEG7", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="W1BEG3", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="WW4BEG1", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JW2BEG1", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JS2BEG5", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="EE4BEG1", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="A", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="E6BEG0", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JN2BEG2", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JE2BEG1", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JW2BEG7", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="JN2BEG5", tile=Tile(x=1, y=1))], [NodeHeader(name="LA_O", tile=Tile(x=1, y=1)), NodeHeader(name="W6BEG0", tile=Tile(x=1, y=1))]]

        file = "tb_test/.FABulous/pips.txt"
        nodes = get_nodes_from_file_for_tile(file, tile, mapping)
        graph = add_parents_and_children_for_tile(file, tile, nodes, mapping)
        mapping.node_header_to_uid
        paths = [[NodeHeader("LA_O", tile)]]
        visited = set()
        node = mapping.node_header_to_uid[NodeHeader("LA_O", Tile(1, 1))]
        #paths = [[NodeHeader("LA_O", tile)]]
        paths = [[node]]

        visited.add(node)

        #Act
        append_paths(paths, node, graph, visited)

        #Assert
        paths_node_header = []
        for path in paths:
            header_path = []
            for node in path:
                header_path.append(mapping.uid_to_node_header[node])
            paths_node_header.append(header_path)
        self.assertCountEqual(paths_node_header, target_paths)

    def test_empty_paths(self):
        """Test when paths is an empty list."""
        # Arrange
        paths = []
        current_node = NodeHeader("A", Tile(0, 0))
        graph = {"A": NodeHeader("A", Tile(0, 0))}
        visited = set()

        # Act
        append_paths(paths, current_node, graph, visited)

        # Assert
        self.assertEqual(paths, [])

    def test_no_children(self):
        """Test when the current node has no children."""
        # Arrange
        paths = [[NodeHeader("A", Tile(1, 1))]]
        current_node = NodeHeader("C", Tile(3, 3))
        graph = {"C": NodeHeader("C", Tile(3, 3))}
        visited = set()

        # Act
        append_paths(paths, current_node, graph, visited)

        # Assert
        self.assertEqual(paths, [[NodeHeader("A", Tile(1, 1))]])

    @unittest.skip("Test not yet checked")
    def test_existing_node_in_path(self):
        """Test when the current node is already in the path."""
        # Arrange
        paths = [[NodeHeader("A", Tile(0, 0)), NodeHeader("B", Tile(1, 1))]]
        current_node = NodeHeader("B", Tile(1, 1))
        graph = {"B": NodeHeader("B", Tile(1, 1))}
        visited = set()

        # Act
        append_paths(paths, current_node, graph, visited)

        # Assert
        self.assertEqual(paths, [[NodeHeader("A", Tile(0, 0)), NodeHeader("B", Tile(1, 1))]])

    @unittest.skip("Test not yet checked")
    def test_append_internal_children(self):
        """Test appending internal children to paths."""
        # Arrange
        paths = [[NodeHeader("A", Tile(0, 0))]]
        current_node = NodeHeader("A", Tile(0, 0))
        graph = {"A": NodeHeader("A", Tile(0, 0))}
        visited = set()

        # Act
        append_paths(paths, current_node, graph, visited)

        # Assert
        self.assertEqual(paths, [[NodeHeader("A", Tile(0, 0))]])

    @unittest.skip("Test not yet checked")
    def test_append_external_children(self):
        """Test appending external children to paths."""
        # Arrange
        paths = [[NodeHeader("A", Tile(0, 0))]]
        current_node = NodeHeader("A", Tile(0, 0))
        graph = {"A": NodeHeader("A", Tile(0, 0))}
        visited = set()

        # Act
        append_paths(paths, current_node, graph, visited)

        # Assert
        self.assertEqual(paths, [[NodeHeader("A", Tile(0, 0))]])


    @unittest.skip("Test not yet checked")
    def test_append_both_internal_and_external_children(self):
        """Test appending both internal and external children to paths."""
        # Arrange
        paths = [[NodeHeader("A", Tile(0, 0))]]
        current_node = NodeHeader("A", Tile(0, 0))
        graph = {"A": NodeHeader("A", Tile(0, 0))}
        visited = set()

        # Act
        append_paths(paths, current_node, graph, visited)

        # Assert
        self.assertEqual(paths, [[NodeHeader("A", Tile(0, 0))]])

    @unittest.skip("Test not yet checked")
    def test_visited_nodes(self):
        """Test when some nodes are already visited."""
        # Arrange
        paths = [[NodeHeader("A", Tile(0, 0))]]
        current_node = NodeHeader("A", Tile(0, 0))
        graph = {"A": NodeHeader("A", Tile(0, 0))}
        visited = {"B"}

        # Act
        append_paths(paths, current_node, graph, visited)

        # Assert
        self.assertEqual(paths, [[NodeHeader("A", Tile(0, 0))]])

    @unittest.skip("Test not yet checked")
    def test_multiple_paths(self):
        """Test when there are multiple paths to append."""
        # Arrange
        paths = [
            [NodeHeader("A", Tile(0, 0)), NodeHeader("B", Tile(1, 1))],
            [NodeHeader("C", Tile(2, 2)), NodeHeader("D", Tile(3, 3))]
        ]
        current_node = NodeHeader("E", Tile(4, 4))
        graph = {
            "B": NodeHeader("B", Tile(1, 1)),
            "D": NodeHeader("D", Tile(3, 3)),
        }
        visited = set()

        # Act
        append_paths(paths, current_node, graph, visited)

        # Assert
        self.assertEqual(paths, [
            [NodeHeader("A", Tile(0, 0)), NodeHeader("B", Tile(1, 1)), NodeHeader("E", Tile(4, 4))],
            [NodeHeader("C", Tile(2, 2)), NodeHeader("D", Tile(3, 3)), NodeHeader("E", Tile(4, 4))]
        ])

    @unittest.skip("Test not yet checked")
    def test_complex_scenario(self):
        """Test a more complex scenario with various conditions."""
        # Arrange
        paths = [
            [NodeHeader("A", Tile(0, 0)), NodeHeader("B", Tile(1, 1))],
            [NodeHeader("C", Tile(2, 2)), NodeHeader("D", Tile(3, 3))]
        ]
        current_node = NodeHeader("E", Tile(4, 4))
        graph = {
            "B": NodeHeader("B", Tile(1, 1)),
            "D": NodeHeader("D", Tile(3, 3)),
            "G": NodeHeader("G", Tile(5, 5)),
        }
        visited = {"F"}

        # Act
        append_paths(paths, current_node, graph, visited)

        # Assert
        self.assertEqual(paths, [
            [NodeHeader("A", Tile(0, 0)), NodeHeader("B", Tile(1, 1)), NodeHeader("E", Tile(4, 4))],
            [NodeHeader("C", Tile(2, 2)), NodeHeader("D", Tile(3, 3)), NodeHeader("E", Tile(4, 4))],
            [NodeHeader("G", Tile(5, 5)), NodeHeader("E", Tile(4, 4))],
        ])
       '''

if __name__ == "__main__":
    unittest.main()
