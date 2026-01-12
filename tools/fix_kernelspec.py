"""
Fix kernelspec display names for all notebooks.

This script updates the kernelspec display name to 'Python 3' for all notebooks
in the project to ensure consistent kernel display across different environments.
"""

import os
import nbformat

from generate_contents import iter_notebooks, NOTEBOOK_DIR


def fix_kernelspec():
    """Update kernelspec display name to 'Python 3' for all notebooks."""
    for nb_name in iter_notebooks():
        nb_file = os.path.join(NOTEBOOK_DIR, nb_name)
        nb = nbformat.read(nb_file, as_version=4)

        print(f"- Updating kernelspec for {nb_name}")
        
        # Ensure kernelspec metadata exists
        if 'kernelspec' not in nb['metadata']:
            nb['metadata']['kernelspec'] = {}
        
        nb['metadata']['kernelspec']['display_name'] = 'Python 3'

        nbformat.write(nb, nb_file)


if __name__ == '__main__':
    fix_kernelspec()
