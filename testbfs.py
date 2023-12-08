#!/bin/python
import sys
import unittest
from unittest.mock import Mock
from unittest.mock import patch

from search_path.bfs import SearchPath
from fabric_generator.file_parser import parseMatrix
from search_path.utils import transpose_csv, create_data
from search_path.graph import *

generic_dir = "./fabric_files/generic/"
csvfile = "./tb_test/Tile/LUT4AB/" + "LUT4AB_switch_matrix.csv"
csvfile_transposed = "./tb_test/Tile/LUT4AB/" + "LUT4AB_switch_matrix_transposed.csv"

class TestBfs(unittest.TestCase):
    data = parseMatrix(csvfile, "LUT4AB")
    data_transposed = parseMatrix(csvfile_transposed, "LUT4AB")
    sp = SearchPath(data, data_transposed)
    best = sp.Path(list(), sys.maxsize)
    current_path = sp.Path(list(), 0)

    def setUp(self):
        self.data_transposed = parseMatrix(csvfile, "LUT4AB")
        transpose_csv(csvfile, csvfile_transposed)
        self.best = self.sp.Path(list(), sys.maxsize)
        self.current_path = self.sp.Path(list(), 0)

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
        graph = create_graph_from_file("tb_test/.FABulous/pips.txt")
        #graph.find_path("X1Y1", "LA_O", "X1Y1", "LA_I3")
        print(graph.nodes["X1Y1"]["LA_O"])
if __name__ == '__main__':
    unittest.main()
