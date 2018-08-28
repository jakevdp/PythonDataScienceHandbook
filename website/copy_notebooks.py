"""
This script copies all notebooks from the book into the website directory, and
creates pages which wrap them and link together.
"""
import os
import nbformat
import shutil

PAGEFILE = """title: {title}
url:
save_as: {htmlfile}
Template: {template}

{{% notebook notebooks/{notebook_file} cells[{cells}] %}}
"""

INTRO_TEXT = """This website contains the full text of the [Python Data Science Handbook](http://shop.oreilly.com/product/0636920034919.do) by Jake VanderPlas; the content is available [on GitHub](https://github.com/jakevdp/PythonDataScienceHandbook) in the form of Jupyter notebooks.

The text is released under the [CC-BY-NC-ND license](https://creativecommons.org/licenses/by-nc-nd/3.0/us/legalcode), and code is released under the [MIT license](https://opensource.org/licenses/MIT).

If you find this content useful, please consider supporting the work by [buying the book](http://shop.oreilly.com/product/0636920034919.do)!
"""


def abspath_from_here(*args):
    here = os.path.dirname(__file__)
    path = os.path.join(here, *args)
    return os.path.abspath(path)

NB_SOURCE_DIR = abspath_from_here('..', 'notebooks')
NB_DEST_DIR = abspath_from_here('content', 'notebooks')
PAGE_DEST_DIR = abspath_from_here('content', 'pages')


def copy_notebooks():
    if not os.path.exists(NB_DEST_DIR):
        os.makedirs(NB_DEST_DIR)
    if not os.path.exists(PAGE_DEST_DIR):
        os.makedirs(PAGE_DEST_DIR)

    nblist = sorted(nb for nb in os.listdir(NB_SOURCE_DIR)
                    if nb.endswith('.ipynb'))
    name_map = {nb: nb.rsplit('.', 1)[0].lower() + '.html'
                for nb in nblist}

    figsource = abspath_from_here('..', 'notebooks', 'figures')
    figdest = abspath_from_here('content', 'figures')

    if os.path.exists(figdest):
        shutil.rmtree(figdest)
    shutil.copytree(figsource, figdest)

    figurelist = os.listdir(abspath_from_here('content', 'figures'))
    figure_map = {os.path.join('figures', fig) : os.path.join('/PythonDataScienceHandbook/figures', fig)
                  for fig in figurelist}

    for nb in nblist:
        base, ext = os.path.splitext(nb)
        print('-', nb)

        content = nbformat.read(os.path.join(NB_SOURCE_DIR, nb),
                                as_version=4)

        if nb == 'Index.ipynb':
            # content[0] is the title
            # content[1] is the cover image
            # content[2] is the license
            cells = '1:'
            template = 'page'
            title = 'Python Data Science Handbook'
            content.cells[2].source = INTRO_TEXT
        else:
            # content[0] is the book information
            # content[1] is the navigation bar
            # content[2] is the title
            cells = '2:'
            template = 'booksection'
            title = content.cells[2].source
            if not title.startswith('#') or len(title.splitlines()) > 1:
                raise ValueError('title not found in third cell')
            title = title.lstrip('#').strip()

            # put nav below title
            content.cells.insert(0, content.cells.pop(2))

        # Replace internal URLs and figure links in notebook
        for cell in content.cells:
            if cell.cell_type == 'markdown':
                for nbname, htmlname in name_map.items():
                    if nbname in cell.source:
                        cell.source = cell.source.replace(nbname, htmlname)
                for figname, newfigname in figure_map.items():
                    if figname in cell.source:
                        cell.source = cell.source.replace(figname, newfigname)
            if cell.source.startswith("<!--NAVIGATION-->"):
                # Undo replacement of notebook link in the colab badge
                cell.source = nb.join(cell.source.rsplit(name_map[nb], 1))

        nbformat.write(content, os.path.join(NB_DEST_DIR, nb))

        pagefile = os.path.join(PAGE_DEST_DIR, base + '.md')
        htmlfile = base.lower() + '.html'
        with open(pagefile, 'w') as f:
            f.write(PAGEFILE.format(title=title,
                                    htmlfile=htmlfile,
                                    notebook_file=nb,
                                    template=template,
                                    cells=cells))

if __name__ == '__main__':
    copy_notebooks()
