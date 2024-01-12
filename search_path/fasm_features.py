#!/bin/python

from more_itertools import peekable
from typing import List

def create_features(path: List) -> List:
    """ Create the FASM features from the given path.

    :param List path: The path for which to create the FASM features.
    :return: All features created from the path.
    :rtype: List
    """
    feature_list = []
    path = peekable(path)
    for elem in path:
        if path:
            tile = elem.tile
            tile_str = tile.to_string()
            source = elem.name

            next_elem = path.peek()
            sink = next_elem.name

            feature = f'{tile_str}.{source}.{sink}'
            feature_list.append(feature)

    return feature_list

def append_features_to_file(features: List, file: str) -> None:
    """Append the features to an existing file.

    :param List features: The features to append to the file.
    :param str file: The file where to append the features to.
    """
    found_start = False
    with open(file, 'r+') as f:
        for line in iter(f.readline, ''):
            if '#additional features' in line:
                f.seek(0, 1)
                f.truncate()
                found_start = True
                break

        if not found_start:
            f.write('#additional features\n')
        previous_tile = ""
        for feature in features:
            current_tile = extract_start_tile_from_feature(feature)
            if previous_tile != current_tile:
                f.write(f"\n#Path for {current_tile}:\n")
            f.write(feature + '\n')
            previous_tile = current_tile

def extract_start_tile_from_feature(feature: str):
    """ Extract the start tile of a wire from a feature.

    :param str feature: The feature where to extract the start tile from.
    :return: The start tile of the wire.
    :rtype: str
    """
    return feature.split('.')[0]

if __name__ == "__main__":
    pass
