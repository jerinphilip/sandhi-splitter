"""
Code to train the model using given dataset.
"""
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
import json
import argparse
from sandhisplitter.model import Model
from sandhisplitter.util import extract
from io import open


def main():
    # if __name__ == '__main__':  # pragma: no cover
    parser = argparse.ArgumentParser(description="Train a model")
    arguments = [
        ["-k", "--depth", "depth of the trie", int, "depth"],
        ["-s", "--skip", "initial skip", int, "skip"],
        ["-i", "--trainfile", "path to training file",
            str, "trainfile"],
        ["-o", "--outputfile", "path to store model",
            str, "modelfile"],
    ]

    # Add options
    for arg in arguments:
        unix, gnu, desc, typename, dest = arg
        parser.add_argument(unix, gnu, help=desc, type=typename,
                            required=True, dest=dest)

    args = parser.parse_args()

    # Load training file and add entries to model
    data = open(args.trainfile, "r", encoding="utf-8")
    line_number = 0
    model = Model(depth=args.depth, skip=args.skip)
    try:
        for line in data:
            line = line.strip()
            line_number += 1
            word, splits, locs = extract(line)
            model.add_entry(word, splits, locs)
    except:
        print("Input file syntax error in line %d" % (line_number))
        raise

    # Serialize the model and export to file
    exported = model.serialize()
    output_file = open(args.modelfile, "w", encoding="utf-8")
    result = json.dumps(exported, ensure_ascii=False)
    output_file.write(result)
