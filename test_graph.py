import unittest
from search_path.bfs import append_paths
from search_path.node import NodeHeader
from search_path.tile import Tile

class TestAppendPaths(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()

