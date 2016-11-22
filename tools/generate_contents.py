import os
import re
import itertools
import nbformat

NOTEBOOK_DIR = os.path.join(os.path.dirname(__file__), '..', 'notebooks')

CHAPTERS = {"00": "Preface",
            "01": "IPython: Beyond Normal Python",
            "02": "NumPy",
            "03": "Pandas",
            "04": "Matplotlib",
            "05": "Machine Learning"}

REG = re.compile(r'(\d\d)\.(\d\d)-(.*)\.ipynb')


def iter_notebooks():
    return sorted(nb for nb in os.listdir(NOTEBOOK_DIR) if REG.match(nb))


def get_notebook_title(nb_file):
    nb = nbformat.read(os.path.join(NOTEBOOK_DIR, nb_file), as_version=4)
    for cell in nb.cells:
        if cell.source.startswith('#'):
            return cell.source[1:].splitlines()[0].strip()


def gen_contents(directory=None):
    for nb in iter_notebooks():
        if directory:
            nb_url = os.path.join(directory, nb)
        else:
            nb_url = nb
        chapter, section, title = REG.match(nb).groups()
        title = get_notebook_title(nb)
        if section == '00':
            if chapter in ['00', '06']:
                yield '\n### [{0}]({1})'.format(title, nb_url)
            else:
                yield '\n### [{0}. {1}]({2})'.format(int(chapter),
                                                     title, nb_url)
        else:
            yield "- [{0}]({1})".format(title, nb_url)


def print_contents(directory=None):
    print('\n'.join(gen_contents(directory)))


if __name__ == '__main__':
    print_contents()
    print('\n', 70 * '#', '\n')
    print_contents('http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/')
