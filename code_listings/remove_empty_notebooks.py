import os
import io
import glob

import nbformat


def count_cells(filename):
    with io.open(filename, 'r', encoding='utf8') as f:
        nb = nbformat.read(f, as_version=4)
    return len(nb.cells)



for filename in glob.glob('0[0-6].[0-9][0-9]-*.ipynb'):
    if count_cells(filename) < 2:
        print("removing", filename)
        os.remove(filename)
