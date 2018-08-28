import os
import itertools

from ipykernel import kernelspec as ks
import nbformat
from nbformat.v4.nbbase import new_markdown_cell

from generate_contents import NOTEBOOK_DIR, REG, iter_notebooks, get_notebook_title

COLAB_COMMENT = "<!--COLAB_LINK-->"
NAV_COMMENT = "<!--NAVIGATION-->\n"

COLAB_LINK_TEMPLATE = COLAB_COMMENT + """
<p><a href="https://colab.research.google.com/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/{notebook_filename}"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open and Execute in Google Colaboratory"></a></p>
"""

def write_colab_links():
    for nb_name in iter_notebooks():
        print(nb_name)
        nb_filename = os.path.basename(nb_name)
        nb = nbformat.read(nb_name, as_version=4)
        is_navbar = lambda cell: cell.source.startswith(NAV_COMMENT)
        is_colab_link = lambda cell: cell.source.startswith(COLAB_COMMENT)

        if is_navbar(nb.cells[1]):
            colab_link = COLAB_LINK_TEMPLATE.format(
                notebook_filename=nb_filename)
            
            if is_colab_link(nb.cells[2]):
                print("- amending colab link for {0}".format(nb_filename))
                nb.cells[2].source = colab_link
            else:
                print("- inserting colab link for {0}".format(nb_filename))
                nb.cells.insert(2, new_markdown_cell(source=colab_link))
        else:
            print("- no navbar found in {0}".format(nb_filename))

        nbformat.write(nb, nb_name)


if __name__ == '__main__':
    write_colab_links()
