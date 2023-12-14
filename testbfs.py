#!/bin/python
import sys
import os
import unittest
import time
from unittest.mock import Mock
from unittest.mock import patch

from search_path.graph import *

test_file = "test_features.txt"

class TestBfs(unittest.TestCase):

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.6f' % (self.id(), t))

        #Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

    '''
    @patch('search_path.bfs.SearchPath.beg_to_end')
    def test_end_to_beg(self, mock_beg_to_end):
        mock_beg_to_end.return_value = False

        retval = self.sp.end_to_beg("J_l_AB_END3", "LA_I3", self.best, self.current_path)
        self.assertTrue(retval, "Expected True, got False")
        self.assertTrue(self.best.cost == 1, f"Expected {1} got {self.best.cost}")

    @patch('search_path.bfs.SearchPath.end_to_beg')
    def test_beg_to_end(self, mock_end_to_beg):
        mock_end_to_beg.return_value = False

        retval = self.sp.beg_to_end("J_l_AB_BEG3" ,"J_l_AB_END3", self.best, self.current_path)
        self.assertTrue(retval, "Expected True, got False")
        self.assertTrue(self.best.cost == 1, f"Expected {1} got {self.best.cost}")

    '''
    def test_create_graph_from_file(self):
        #graph = create_graph_from_file("tb_test/.FABulous/pips.txt")
        #Arrange
        file = "tb_test/.FABulous/pips.txt"
        tile = Tile(1,1)
        nodes = get_nodes_from_file_for_tile(file, tile)
        nodes = add_parents_and_children(file, tile, nodes)

        found_target = False
        name = ""
        #Act
        if "JW2BEG1" in nodes["LA_O"].internal_children:
            if "JW2END1" in nodes["JW2BEG1"].internal_children:
                if "J_l_AB_BEG3" in nodes["JW2END1"].internal_children:
                    if "J_l_AB_END3" in nodes["J_l_AB_BEG3"].internal_children:
                        if "LA_I3" in nodes["J_l_AB_END3"].internal_children:
                            found_target = True
                            name = nodes["LA_I3"].name
        #Assert
        self.assertEqual("LA_I3", name)
        self.assertTrue(found_target)

    def test_str_to_tile(self):
        #Act
        tile = str_to_tile("X1Y1")
        #Assert
        self.assertEqual(tile.x, 1)
        self.assertEqual(tile.y, 1)
        #Act
        tile = str_to_tile("X12Y13")
        #Assert
        self.assertEqual(tile.x, 12)
        self.assertEqual(tile.y, 13)

    def test_tile_to_str(self):
        #Arrange
        tile = Tile(1, 1)
        #Act
        tile_str = tile_to_str(tile)
        #Assert
        self.assertEqual("X1Y1", tile_str)
        #Arrange
        tile = Tile(999, 999)
        #Act
        tile_str = tile_to_str(tile)
        #Assert
        self.assertEqual("X999Y999", tile_str)

    def test_bfs(self):
        #Arrange
        start_node = "LA_O"
        end_node = "LA_I3"
        target_path = ["LA_O", "JW2BEG1", "JW2END1", "J_l_AB_BEG3", "J_l_AB_END3", "LA_I3"]
        file = "tb_test/.FABulous/pips.txt"
        tile = Tile(1,1)
        nodes = get_nodes_from_file_for_tile(file, tile)
        graph = add_parents_and_children(file, tile, nodes)
        #Act
        path = bfs(graph, start_node, end_node)
        #Assert
        self.assertTrue(target_path in path)

    def test_append_paths(self):
        #Arrange
        paths = [["LA_O"]]
        target_paths = [['LA_O'], ['LA_O', 'JN2BEG6'], ['LA_O', 'NN4BEG1'], ['LA_O', 'JW2BEG4'], ['LA_O', 'JW2BEG6'], ['LA_O', 'E6BEG0'], ['LA_O', 'EE4BEG1'], ['LA_O', 'JW2BEG7'], ['LA_O', 'JN2BEG4'], ['LA_O', 'JS2BEG1'], ['LA_O', 'SS4BEG1'], ['LA_O', 'JE2BEG3'], ['LA_O', 'JW2BEG2'], ['LA_O', 'JS2BEG5'], ['LA_O', 'JN2BEG7'], ['LA_O', 'JE2BEG5'], ['LA_O', 'JE2BEG6'], ['LA_O', 'S4BEG0'], ['LA_O', 'A'], ['LA_O', 'W6BEG0'], ['LA_O', 'JE2BEG7'], ['LA_O', 'W1BEG3'], ['LA_O', 'JS2BEG7'], ['LA_O', 'JN2BEG3'], ['LA_O', 'JW2BEG3'], ['LA_O', 'JE2BEG1'], ['LA_O', 'WW4BEG1'], ['LA_O', 'E6BEG1'], ['LA_O', 'JS2BEG6'], ['LA_O', 'JE2BEG4'], ['LA_O', 'JS2BEG2'], ['LA_O', 'JE2BEG2'], ['LA_O', 'JW2BEG5'], ['LA_O', 'JN2BEG2'], ['LA_O', 'JN2BEG5'], ['LA_O', 'JW2BEG1'], ['LA_O', 'JN2BEG1'], ['LA_O', 'JS2BEG3'], ['LA_O', 'JS2BEG4'], ['LA_O', 'W6BEG1']]

        file = "tb_test/.FABulous/pips.txt"
        tile = Tile(1,1)
        nodes = get_nodes_from_file_for_tile(file, tile)
        graph = add_parents_and_children(file, tile, nodes)
        visited = set()
        visited.add("LA_0")

        #Act
        append_paths(paths, "LA_O", graph, visited)

        #Assert
        self.assertCountEqual(paths, target_paths)

    def test_get_lists_where_last_element_machtes(self):
        #Arrange
        lists = [["1"], ["1", "2"], ["1", "2", "3"], ["1", "2", "3", "4"]]

        #Act
        result = get_lists_where_last_element_matches(lists, "4")

        #Assert
        self.assertCountEqual(result,  [["1", "2", "3", "4"]])

    def test_create_features(self):
        #Arrange
        target_path = ["LA_O", "JW2BEG1", "JW2END1", "J_l_AB_BEG3", "J_l_AB_END3", "LA_I3"]
        target_features = ["LA_O.JW2BEG1", "JW2BEG1.JW2END1", "JW2END1.J_l_AB_BEG3", "J_l_AB_BEG3.J_l_AB_END3", "J_l_AB_END3.LA_I3"]
        #Act
        features = create_features(target_path)
        #Assert
        self.assertCountEqual(target_features, features)

    def test_append_features_to_file(self):
        #Arrange
        features = ["LA_O.JW2BEG1", "JW2BEG1.JW2END1", "JW2END1.J_l_AB_BEG3", "J_l_AB_BEG3.J_l_AB_END3", "J_l_AB_END3.LA_I3"]
        self.assertFalse(os.path.exists(test_file))
        open(test_file, 'w').close()
        start_found = False

        #Act
        append_features_to_file(features, test_file)

        #Assert
        with open(test_file, 'r') as f:
            index = 0
            for line in f:
                if start_found:
                    self.assertEqual(line.rstrip('\n'), features[index])
                    index += 1
                if line.startswith("# additional features"):
                    start_found = True

if __name__ == '__main__':
    unittest.main()
