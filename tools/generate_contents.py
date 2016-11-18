import os
import re
import itertools

PREV_TEMPLATE = " <[{title}]({url}) "
CONTENTS = "| [Contents](Index.ipynb)| "
NEXT_TEMPLATE = " [{title}](url) >"

NOTEBOOK_DIR = os.path.join(os.path.dirname(__file__), '..', 'notebooks')

CHAPTERS = {"00": "Preface",
            "01": "IPython: Beyond Normal Python",
            "02": "NumPy",
            "03": "Pandas",
            "04": "Matplotlib",
            "05": "Machine Learning"}

REG = re.compile(r'(\d\d)\.(\d\d)-(.*)\.ipynb')

notebooks = sorted(nb for nb in os.listdir(NOTEBOOK_DIR) if REG.match(nb))

def prev_this_next(it):
    a, b, c = itertools.tee(it,3)
    next(c)
    return zip(itertools.chain([None], a), b, itertools.chain(c, [None]))




def iter_navbars(notebooks):
    for prev_nb, nb, next_nb in prev_this_next(notebooks):
        navbar = ""
        if prev_nb:
            navbar += PREV_TEMPLATE.format(title=REG.match(prev_nb).groups()[2],
                                           url=prev_nb)
        navbar += CONTENTS
        if next_nb:
            navbar += NEXT_TEMPLATE.format(title=REG.match(next_nb).groups()[2],
                                           url=next_nb)
        yield navbar


def gen_contents(notebooks):
    def get_chapter(nb):
        return REG.match(nb).groups()[0]
    
    for nb in notebooks:
        chapter, section, title = REG.match(nb).groups()
        title = title.replace('-', ' ')
        if section == '00':
            yield '\n### [{0}]({1})'.format(title, nb)
        else:
            yield "- [{0}]({1})".format(title, nb)


print('\n'.join(gen_contents(notebooks)))
