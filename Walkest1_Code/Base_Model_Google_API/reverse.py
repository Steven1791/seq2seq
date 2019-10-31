#!/usr/bin/env python3

import io
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input', help="reverses line order of this text file")
args = parser.parse_args()

text = args.input
newTextFile = os.path.dirname(args.input) + "/" + os.path.basename(args.input) + "_reversed.txt"

with open (text, 'r') as text:
    lines = text.readlines()
    lines.reverse()

with open (newTextFile, 'w') as newText:
    newText.writelines(lines)

