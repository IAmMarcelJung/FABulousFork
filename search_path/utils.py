#!/bin/python
import os

def transpose_csv(input_file, output_file):
    if os.path.isfile(output_file):
        return
    with open(input_file, "r") as f_in:
        a = zip(*csv.reader(f_in))

    with open(output_file, "w") as f_out:
        csv.writer(f_out).writerows(a)

def create_data(project_dir):
    pip_file = project_dir + ".FABulous/pips.txt"
    with open(pip_file, "r") as f:
        for line in f:
            if line.startswith('#'):
                continue
            line_list = line.split(',')
            tile = line_list[0]
            feature = line_list[-1]

def test(project_dir):
    pip_file = project_dir + ".FABulous/pips.txt"
    with open(pip_file) as f:
        for line in f:
            # Skip lines starting with '#'
            if not line.startswith('#'):
                # Extract source, destination, and feature
                source_tile, _, destination_tile, _, _, feature = line.split(',')

                # Create the key (source, destination) tuple
                key = (source_tile, destination_tile)

                # Store the feature value
                connections_dict[key] = feature

if __name__ == "__main__":
    pass
