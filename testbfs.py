#!/bin/python
import sys
import os
import unittest
import time
import cProfile
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
        tile_str = tile_to_str(tile)

        found_target = False
        name = ""
        #Act
        if Node_Header("JW2BEG1", tile) in nodes[Node_Header("LA_O", tile)].internal_children:
            if Node_Header("JW2END1", tile) in nodes[Node_Header("JW2BEG1", tile)].internal_children:
                if Node_Header("J_l_AB_BEG3", tile) in nodes[Node_Header("JW2END1", tile)].internal_children:
                    if Node_Header("J_l_AB_END3", tile) in nodes[Node_Header("J_l_AB_BEG3", tile)].internal_children:
                        if Node_Header("LA_I3", tile) in nodes[Node_Header("J_l_AB_END3", tile)].internal_children:
                            found_target = True
        name = nodes[Node_Header("LA_I3", tile)].name
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
        tile = Tile(1, 1)
        start_node = Node_Header("LA_O", tile)
        end_node = Node_Header("LA_I3", tile)
        target_path = [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JW2BEG1', tile=Tile(x=1, y=1)), Node_Header(name='JW2END1', tile=Tile(x=1, y=1)), Node_Header(name='J_l_AB_BEG3', tile=Tile(x=1, y=1)), Node_Header(name='J_l_AB_END3', tile=Tile(x=1, y=1)), Node_Header(name='LA_I3', tile=Tile(x=1, y=1))]
        file = "tb_test/.FABulous/pips.txt"
        nodes = get_nodes_from_file_for_tile(file, tile)
        graph = add_parents_and_children(file, tile, nodes)
        #Act
        cProfile.runctx('bfs(graph, start_node, end_node)', globals(), locals(), "profile.txt", 'cumtime')
        paths = bfs(graph, start_node, end_node)
        #Assert
        self.assertTrue(target_path in paths, "Could not find path from LA_O to LA_I3")

        #Arrange
        start_node = Node_Header("E6END0", tile)
        end_tile = Tile(0, 1)
        end_node = Node_Header("W2MID3", end_tile)
        target_path = [Node_Header('E6END0', tile), Node_Header('JW2BEG3', tile), Node_Header('JW2END3', tile), Node_Header('W2BEG3', tile), Node_Header('W2MID3', end_tile)]
        #Act
        paths = bfs(graph, start_node, end_node)
        #Assert
        self.assertTrue(target_path in paths, "Could not find path from E6END0 to W2MID3")

        #Arrange
        start_node = Node_Header("E1END0", tile)
        end_node = Node_Header("LA_I0", tile)
        target_path = [Node_Header('E1END0', tile), Node_Header('JN2BEG1', tile), Node_Header('JN2END1', tile), Node_Header('J_l_AB_BEG0', tile), Node_Header('J_l_AB_END0', tile), Node_Header('LA_I0', tile)]
        #Act
        paths = bfs(graph, start_node, end_node)
        #Assert
        self.assertTrue(target_path in paths, "Could not find path from E1END0 to LA_I0")

    def test_append_paths(self):
        #Arrange
        tile = Tile(1,1)
        paths = [[Node_Header("LA_O", tile)]]
        target_paths = [[Node_Header(name='LA_O', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JS2BEG1', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JE2BEG5', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JW2BEG5', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JE2BEG6', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='S4BEG0', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JS2BEG2', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='SS4BEG1', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JW2BEG3', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JW2BEG6', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JW2BEG4', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JS2BEG4', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JN2BEG4', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='E6BEG1', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JN2BEG1', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JN2BEG6', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JW2BEG2', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JE2BEG4', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JN2BEG7', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JS2BEG6', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JE2BEG2', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JS2BEG3', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JS2BEG7', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='NN4BEG1', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JN2BEG3', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='W6BEG1', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JE2BEG3', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JE2BEG7', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='W1BEG3', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='WW4BEG1', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JW2BEG1', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JS2BEG5', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='EE4BEG1', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='A', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='E6BEG0', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JN2BEG2', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JE2BEG1', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JW2BEG7', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='JN2BEG5', tile=Tile(x=1, y=1))], [Node_Header(name='LA_O', tile=Tile(x=1, y=1)), Node_Header(name='W6BEG0', tile=Tile(x=1, y=1))]]

        file = "tb_test/.FABulous/pips.txt"
        nodes = get_nodes_from_file_for_tile(file, tile)
        graph = add_parents_and_children(file, tile, nodes)
        visited = set()
        node = Node_Header("LA_O", Tile(1, 1))

        visited.add(node)

        #Act
        append_paths(paths, node, graph, visited)

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
