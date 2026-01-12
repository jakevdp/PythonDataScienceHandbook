"""
Add navigation bars to all notebooks.

This script adds previous/next navigation links and Colab badges to all notebooks
in the project to improve user experience when browsing through the content.
"""

import os
import itertools

from ipykernel import kernelspec as ks
import nbformat
from nbformat.v4.nbbase import new_markdown_cell

from generate_contents import NOTEBOOK_DIR, REG, iter_notebooks, get_notebook_title


def prev_this_next(it):
    """
    Generate previous, current, and next items from an iterator.
    
    Parameters
    ----------
    it : iterator
        Iterator to generate triples from
        
    Returns
    -------
    zip object
        Zipped tuples of (previous, current, next) items
    """
    a, b, c = itertools.tee(it, 3)
    next(c)
    return zip(itertools.chain([None], a), b, itertools.chain(c, [None]))


PREV_TEMPLATE = "< [{title}]({url}) "
CONTENTS = "| [Contents](Index.ipynb) |"
NEXT_TEMPLATE = " [{title}]({url}) >"
NAV_COMMENT = "<!--NAVIGATION-->\n"

COLAB_LINK = """

<a href="https://colab.research.google.com/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/{notebook_filename}"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open and Execute in Google Colaboratory"></a>
"""


def iter_navbars():
    """
    Generate navigation bars for all notebooks.
    
    Yields
    ------
    tuple
        (notebook_path, navigation_bar) for each notebook
    """
    for prev_nb, nb, next_nb in prev_this_next(iter_notebooks()):
        navbar = NAV_COMMENT
        if prev_nb:
            navbar += PREV_TEMPLATE.format(title=get_notebook_title(prev_nb),
                                           url=prev_nb)
        navbar += CONTENTS
        if next_nb:
            navbar += NEXT_TEMPLATE.format(title=get_notebook_title(next_nb),
                                           url=next_nb)

        navbar += COLAB_LINK.format(notebook_filename=os.path.basename(nb))
            
        yield os.path.join(NOTEBOOK_DIR, nb), navbar


def write_navbars():
    """Write navigation bars to the beginning and end of all notebooks."""
    for nb_name, navbar in iter_navbars():
        nb = nbformat.read(nb_name, as_version=4)
        nb_file = os.path.basename(nb_name)
        is_comment = lambda cell: cell.source.startswith(NAV_COMMENT)

        # Add navbar at the beginning (after potential book info)
        if len(nb.cells) > 1 and is_comment(nb.cells[1]):
            print(f"- amending navbar for {nb_file}")
            nb.cells[1].source = navbar
        else:
            print(f"- inserting navbar for {nb_file}")
            nb.cells.insert(1, new_markdown_cell(source=navbar))

        # Add navbar at the end
        if nb.cells and is_comment(nb.cells[-1]):
            nb.cells[-1].source = navbar
        else:
            nb.cells.append(new_markdown_cell(source=navbar))
        
        nbformat.write(nb, nb_name)


if __name__ == '__main__':
    write_navbars()
