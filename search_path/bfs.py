#!/bin/python3
import pprint as pp
import pandas as pd
import os
import os.path
import sys
import csv

from collections import deque
from fabric_generator.file_parser import parseList, parseMatrix

'''
def bfs(data, start):
    visited = []
    queue = deque()

    visited.append(start)
    queue.append(start)

    while queue:
        s = queue.popleft()

        for column in data[s]:
            if n.values() == 1:
                if n not in visited:
                    key = n.keys()
                    visited.append(key)
                    queue.append(key)

def read_data_frame(filename):
    df = pd.read_csv(filename)
    # The last two rows are not needed
    df.drop(df.tail(2).index,inplace=True)
    return df

def print_features(name: str, data_frame: pd.DataFrame):
    print(data_frame.columns)
    for column in data_frame.columns:
        print(column)
        for elem in column:
            if elem == name:
                pass

def get_child_nodes(node, data_frame):
    filtered_rows = data_frame[data_frame[node] == 1]
    # Only use the node names
    return  filtered_rows.iloc[:,0].to_list()
'''

class SearchPath:
    def __init__(self, data, data_transposed):
        self.data = data
        self.data_transposed = data_transposed

    class Path():
        def __init__(self, path, cost):
            self.path = path
            self.cost = cost
            self.cost_list = list();
            self.cost_list.append(cost)

        def append(self, elem, cost):
            self.path.append(elem)
            self.cost_list.append(cost)
            self.cost += cost

        def pop(self):
            self.path.pop()
            cost = self.cost_list.pop()
            self.cost -= cost

        def copy(self, source):
            self.path.clear()
            self.cost_list.clear()
            for elem in source.path:
                self.path.append(elem)
            for elem in source.cost_list:
                self.cost_list.append(elem)
            self.cost = source.cost


    def dfs(start, end, data):
        '''
        Search from end to start.
        '''
        first = data[end]
        best = Path(list(), sys.maxsize)
        current_node = end
        current_path = Path(list(), 0)
        print(end)
        current_path.append(end, 1)
        print(current_path.path)
        print(current_path.cost)
        for node in first:
            for key, value in data.items():
                print(key)
                if node in value:
                    current_path.append(key, 1)
        print(current_path.path)


    def end_to_beg(self, target_node, current_node, best, current_path):
        end_nodes = self.data[current_node]
        for node in end_nodes:
            current_path.append(node, 1)
            if current_path.cost > best.cost or current_path.cost > 999:
                return False
            if node == target_node:
                best.copy(current_path)
                return True
            found_start = self.beg_to_end(target_node, current_node, best, current_path)
            if found_start:
                return True

            current_path.pop()
        return False

    def beg_to_end(self, target_node, current_node, best, current_path):
        start_nodes = self.data_transposed[current_node]
        print(start_nodes)
        for node in start_nodes:
            if node in current_path.path:
                continue
            current_path.append(node, 1)
            if current_path.cost > best.cost or current_path.cost > 99:
                return False
                print(current_path.path)
            if node == target_node:
                best.copy(current_path)
                return True
            found_start = self.beg_to_end(target_node, current_node, best, current_path)
            if found_start:
                return True

            current_path.pop()
        return False


    '''
    def beg_to_end(target_node, current_node, best, current_path, data_transposed):
        for key, value in data.items():
            print(value)
            if current_node in value:
                current_path.append(key, 1)
                if key == target_node:
                    best.copy(current_path)
                    return True
                found_start = end_to_beg(target_node, current_node, best, current_path, data)
                if found_start:
                    return True
                current_path.pop()
        return False
        '''
def create_data(self, project_dir):
    pip_file = project_dir + ".FABulous/pips.txt"
    #pip_file = "./tb_test/.FABulous/pips.txt"
    with open(pip_file, "r") as f:
        for line in f:
            if line.startswith('#'):
                print(line)
            line_list = line.split(',')
            tile = line_list[0]
            feature = line_list[-1]


if __name__ == "__main__":
    #df = read_data_frame("LUT4AB_switch_matrix.csv")
    #filtered_data = df[df["N1END0"] == 1]
    #print(df)
    #print(filtered_data)
    #test = filtered_data.loc[:,"N1END0"]
    #test = filtered_data.iloc[:,0]
    #print(get_child_nodes("N1END1", df))
    generic_dir = "./fabric_files/generic/"
    csv = "./tb_test/Tile/LUT4AB/" + "LUT4AB_switch_matrix.csv"
    listfile = generic_dir + "LUT4AB_switch_matrix.list"
    data = parseMatrix(csv, "LUT4AB")

    #first = (data["LA_I0"])
    dfs("LA_O", "LA_I0", data)

    #print(test)
    #print(type(test))
    #print(test.to_list())
    #print(df.loc[:, "N1END0"])
    #print(df.loc[:, "N1END1"])
#    print_features("N1END0", df)

