#!/bin/python
import sys
import os
import unittest
import time
import cProfile
from unittest.mock import Mock
from unittest.mock import patch

from search_path.graph import *
from search_path.utils import *

test_file = "test_features.txt"
fabric_file = "search_path/fabric.csv"

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
        #tile_str = tile_to_str(tile)
        tile_str = tile.to_string()

        found_target = False
        name = ""
        #Act
        if NodeHeader("JW2BEG1", tile) in nodes[NodeHeader("LA_O", tile)].internal_children:
            if NodeHeader("JW2END1", tile) in nodes[NodeHeader("JW2BEG1", tile)].internal_children:
                if NodeHeader("J_l_AB_BEG3", tile) in nodes[NodeHeader("JW2END1", tile)].internal_children:
                    if NodeHeader("J_l_AB_END3", tile) in nodes[NodeHeader("J_l_AB_BEG3", tile)].internal_children:
                        if NodeHeader("LA_I3", tile) in nodes[NodeHeader("J_l_AB_END3", tile)].internal_children:
                            found_target = True
        name = nodes[NodeHeader("LA_I3", tile)].name
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
        tile_str = tile.to_string()
        #Assert
        self.assertEqual("X1Y1", tile_str)
        #Arrange
        tile = Tile(999, 999)
        #Act
        tile_str = tile.to_string()
        #Assert
        self.assertEqual("X999Y999", tile_str)

    @unittest.skip("Skip while testing other test, since this test takes long")
    def test_bfs(self):

        #Arrange
        tile = Tile(1, 1)
        start_node = NodeHeader("LA_O", tile)
        end_node = NodeHeader("LA_I3", tile)
        target_path = [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JW2BEG1', tile=Tile(x=1, y=1)), NodeHeader(name='JW2END1', tile=Tile(x=1, y=1)), NodeHeader(name='J_l_AB_BEG3', tile=Tile(x=1, y=1)), NodeHeader(name='J_l_AB_END3', tile=Tile(x=1, y=1)), NodeHeader(name='LA_I3', tile=Tile(x=1, y=1))]
        file = "tb_test/.FABulous/pips.txt"
        nodes = get_nodes_from_file_for_tile(file, tile)
        graph = add_parents_and_children(file, tile, nodes)
        #Act
        #cProfile.runctx('bfs(graph, start_node, end_node)', globals(), locals(), "profile.txt", 'cumtime')
        paths = bfs(graph, start_node, end_node)
        #Assert
        self.assertTrue(target_path in paths, "Could not find path from LA_O to LA_I3")

        #Arrange
        start_node = NodeHeader("E6END0", tile)
        end_tile = Tile(0, 1)
        end_node = NodeHeader("W2MID3", end_tile)
        target_path = [NodeHeader('E6END0', tile), NodeHeader('JW2BEG3', tile), NodeHeader('JW2END3', tile), NodeHeader('W2BEG3', tile), NodeHeader('W2MID3', end_tile)]
        #Act
        paths = bfs(graph, start_node, end_node)
        #Assert
        self.assertTrue(target_path in paths, "Could not find path from E6END0 to W2MID3")

        #Arrange
        start_node = NodeHeader("E1END0", tile)
        end_node = NodeHeader("LA_I0", tile)
        target_path = [NodeHeader('E1END0', tile), NodeHeader('JN2BEG1', tile), NodeHeader('JN2END1', tile), NodeHeader('J_l_AB_BEG0', tile), NodeHeader('J_l_AB_END0', tile), NodeHeader('LA_I0', tile)]
        #Act
        paths = bfs(graph, start_node, end_node)
        #Assert
        self.assertTrue(target_path in paths, "Could not find path from E1END0 to LA_I0")

    def test_append_paths(self):
        #Arrange
        tile = Tile(1,1)
        paths = [[NodeHeader("LA_O", tile)]]
        target_paths = [[NodeHeader(name='LA_O', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JS2BEG1', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JE2BEG5', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JW2BEG5', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JE2BEG6', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='S4BEG0', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JS2BEG2', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='SS4BEG1', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JW2BEG3', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JW2BEG6', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JW2BEG4', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JS2BEG4', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JN2BEG4', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='E6BEG1', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JN2BEG1', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JN2BEG6', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JW2BEG2', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JE2BEG4', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JN2BEG7', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JS2BEG6', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JE2BEG2', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JS2BEG3', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JS2BEG7', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='NN4BEG1', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JN2BEG3', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='W6BEG1', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JE2BEG3', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JE2BEG7', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='W1BEG3', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='WW4BEG1', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JW2BEG1', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JS2BEG5', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='EE4BEG1', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='A', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='E6BEG0', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JN2BEG2', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JE2BEG1', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JW2BEG7', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JN2BEG5', tile=Tile(x=1, y=1))], [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='W6BEG0', tile=Tile(x=1, y=1))]]

        file = "tb_test/.FABulous/pips.txt"
        nodes = get_nodes_from_file_for_tile(file, tile)
        graph = add_parents_and_children(file, tile, nodes)
        visited = set()
        node = NodeHeader("LA_O", Tile(1, 1))

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
        target_path = [NodeHeader(name='LA_O', tile=Tile(x=1, y=1)), NodeHeader(name='JW2BEG1', tile=Tile(x=1, y=1)), NodeHeader(name='JW2END1', tile=Tile(x=1, y=1)), NodeHeader(name='J_l_AB_BEG3', tile=Tile(x=1, y=1)), NodeHeader(name='J_l_AB_END3', tile=Tile(x=1, y=1)), NodeHeader(name='LA_I3', tile=Tile(x=1, y=1))]
        target_features = ["X1Y1.LA_O.JW2BEG1", "X1Y1.JW2BEG1.JW2END1", "X1Y1.JW2END1.J_l_AB_BEG3", "X1Y1.J_l_AB_BEG3.J_l_AB_END3", "X1Y1.J_l_AB_END3.LA_I3"]
        #Act
        features = create_features(target_path)
        #Assert
        self.assertCountEqual(target_features, features)

    def test_append_features_to_file(self):
        #Arrange
        features = ["X1Y1.LA_O.JW2BEG1", "X1Y1.JW2BEG1.JW2END1", "X1Y1.JW2END1.J_l_AB_BEG3", "X1Y1.J_l_AB_BEG3.J_l_AB_END3", "X1Y1.J_l_AB_END3.LA_I3"]
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
                if line.startswith("#additional features"):
                    if start_found:
                        assertFalse(start_found, 'Found multiple lines containing "#additional features"')
                    start_found = True
        self.assertTrue(start_found)

    def test_get_tiles_for_fabric_return_correct_dict(self):
        #Arrange

        #Act
        tiles = get_tiles_for_fabric(fabric_file)

        #Assert
        self.assertEqual(tiles[Tile(0, 0)], "NULL")
        self.assertEqual(tiles[Tile(9, 0)], "N_term_RAM_IO")
        self.assertEqual(tiles[Tile(0, 15)], "NULL")
        self.assertEqual(tiles[Tile(9, 15)], "S_term_RAM_IO")
        self.assertEqual(tiles[Tile(0, 1)], "W_IO")
        self.assertEqual(tiles[Tile(1, 1)], "LUT4AB")

    def test_get_all_locations_of_tile_type_LUT4AB_return_full_list(self):
        #Arrange
        tile_type = Tile.Types.LUT4AB
        locations_truth = [Tile(1, 1), Tile(2, 1), Tile(4, 1), Tile(5, 1), Tile(7, 1), Tile(8, 1),
                Tile(1, 2), Tile(2, 2), Tile(4, 2), Tile(5, 2), Tile(7, 2), Tile(8, 2),
                Tile(1, 3), Tile(2, 3), Tile(4, 3), Tile(5, 3), Tile(7, 3), Tile(8, 3),
                Tile(1, 4), Tile(2, 4), Tile(4, 4), Tile(5, 4), Tile(7, 4), Tile(8, 4),
                Tile(1, 5), Tile(2, 5), Tile(4, 5), Tile(5, 5), Tile(7, 5), Tile(8, 5),
                Tile(1, 6), Tile(2, 6), Tile(4, 6), Tile(5, 6), Tile(7, 6), Tile(8, 6),
                Tile(1, 7), Tile(2, 7), Tile(4, 7), Tile(5, 7), Tile(7, 7), Tile(8, 7),
                Tile(1, 8), Tile(2, 8), Tile(4, 8), Tile(5, 8), Tile(7, 8), Tile(8, 8),
                Tile(1, 9), Tile(2, 9), Tile(4, 9), Tile(5, 9), Tile(7, 9), Tile(8, 9),
                Tile(1, 10), Tile(2, 10), Tile(4, 10), Tile(5, 10), Tile(7, 10), Tile(8, 10),
                Tile(1, 11), Tile(2, 11), Tile(4, 11), Tile(5, 11), Tile(7, 11), Tile(8, 11),
                Tile(1, 12), Tile(2, 12), Tile(4, 12), Tile(5, 12), Tile(7, 12), Tile(8, 12),
                Tile(1, 13), Tile(2, 13), Tile(4, 13), Tile(5, 13), Tile(7, 13), Tile(8, 13),
                Tile(1, 14), Tile(2, 14), Tile(4, 14), Tile(5, 14), Tile(7, 14), Tile(8, 14)]
        tiles = get_tiles_for_fabric(fabric_file)

        #Act
        locations = get_all_locations_of_tile_type(tile_type, tiles)

        #Assert
        self.assertCountEqual(locations_truth, locations)

    def test_get_all_locations_of_tile_type_NULL_return_full_list(self):
        #Arrange
        tile_type = Tile.Types.NULL
        locations_truth = [Tile(0, 0), Tile(0, 15)]
        tiles = get_tiles_for_fabric(fabric_file)

        #Act
        locations = get_all_locations_of_tile_type(tile_type, tiles)

        #Assert
        self.assertCountEqual(locations_truth, locations)

if __name__ == '__main__':
    unittest.main()
