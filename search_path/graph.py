#!/bin/python
import heapq

class PipeNode:
    def __init__(self, source_tile, source, destination_tile, sink):
        self.source_tile = source_tile
        self.source = source
        self.destination_tile = destination_tile
        self.sink = sink

class PipeGraph:
    def __init__(self):
        self.nodes = {}  # Dictionary to store pipe nodes
        self.edges = {}  # Dictionary to store edges between nodes

    def add_node(self, pipe_node):
        if pipe_node.source_tile not in self.nodes:
            self.nodes[pipe_node.source_tile] = []
        self.nodes[pipe_node.source_tile].append(pipe_node)
        # Add an edge from source to destination
        if pipe_node.destination_tile not in self.edges:
            self.edges[pipe_node.destination_tile] = []
        self.edges[pipe_node.destination_tile].append((pipe_node.source_tile, pipe_node.source))

    def find_path(self, start_tile, start_node, end_tile, end_node):
        # Initialize a set to keep track of visited nodes
        visited = set()
        # Initialize a dictionary to store the shortest distance to each node
        distances = {node: float('inf') for node in self.nodes}
        # Set the distance to the start node to zero
        distances[start_tile] = {start_node: 0}

        # Create a priority queue to store nodes with their distances
        priority_queue = []
        for node in self.nodes[start_tile]:
            print(node.source)
            print(node.sink)
            if node.source == start_node:
                priority_queue.append((distances[start_tile][node.source], start_tile, node.source))

        while priority_queue:
            current_distance, current_tile, current_node = heapq.heappop(priority_queue)

            # If the current node is the destination, we found the path
            if current_tile == end_tile and current_node == end_node:
                path = []
                while current_tile != start_tile:
                    path.append((current_tile, current_node))
                    for neighbor_tile, neighbor_node in self.edges[current_tile]:
                        if neighbor_node == current_node:
                            current_tile = neighbor_tile
                            current_node = None
                            break
                path.append((start_tile, start_node))
                path.reverse()
                return path

            # Mark the current node and tile as visited
            visited.add((current_tile, current_node))

            # Iterate through neighbors and update their distances
            for neighbor_tile, neighbor_node in self.edges[current_tile]:
                if (neighbor_tile, neighbor_node) not in visited:
                    new_distance = current_distance + 1
                    print(type(distances[neighbor_node]))
                    if new_distance < distances[neighbor_tile]:
                        print(distances[neighbor_tile][neighbor_node])
                        distances[neighbor_tile] = new_distance
                        for node in self.nodes[neighbor_tile]:
                            if node.source == neighbor_node:
                                priority_queue.append((new_distance, neighbor_tile, node.source))

def create_graph_from_file(pip_file):
    graph = PipeGraph()
    with open(pip_file) as f:
        for line in f:
            if line.startswith('#'):
                continue
            # Split the line into its components
            source_tile, source, destination_tile, sink, dnc, feature = line.split(',')
            # Create a pipe node and add it to the graph
            pipe_node = PipeNode(source_tile, source, destination_tile, sink)
            graph.add_node(pipe_node)
    return graph

if __name__ == "__main__":
    pass
