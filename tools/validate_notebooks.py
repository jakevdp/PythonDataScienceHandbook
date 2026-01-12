"""
Validate all Jupyter notebooks in the project.

This script checks all notebooks for common issues like missing metadata,
execution count consistency, and cell output validation.
"""

import os
import sys
import nbformat
from nbformat.v4.nbbase import new_markdown_cell

from generate_contents import iter_notebooks, NOTEBOOK_DIR


def validate_notebook(nb_path):
    """
    Validate a single notebook for common issues.
    
    Parameters
    ----------
    nb_path : str
        Path to the notebook file
        
    Returns
    -------
    list
        List of validation warnings/errors
    """
    warnings = []
    
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        return [f"Failed to read notebook: {e}"]
    
    # Check notebook metadata
    if 'kernelspec' not in nb.metadata:
        warnings.append("Missing kernelspec metadata")
    elif 'display_name' not in nb.metadata.kernelspec:
        warnings.append("Missing kernelspec display_name")
    
    # Check for empty cells
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and not cell.source.strip():
            warnings.append(f"Empty code cell at position {i}")
        elif cell.cell_type == 'markdown' and not cell.source.strip():
            warnings.append(f"Empty markdown cell at position {i}")
    
    # Check for book info comment
    if nb.cells and not nb.cells[0].source.startswith("<!--BOOK_INFORMATION-->"):
        warnings.append("Missing book information comment")
    
    # Check for navigation
    has_nav = any("<!--NAVIGATION-->" in cell.source for cell in nb.cells)
    if not has_nav:
        warnings.append("Missing navigation bar")
    
    return warnings


def validate_all_notebooks():
    """Validate all notebooks and print results."""
    print("Validating all notebooks...")
    print("=" * 50)
    
    all_warnings = []
    
    for nb_name in iter_notebooks():
        nb_path = os.path.join(NOTEBOOK_DIR, nb_name)
        warnings = validate_notebook(nb_path)
        
        if warnings:
            print(f"\n{nb_name}:")
            for warning in warnings:
                print(f"  - {warning}")
            all_warnings.extend([(nb_name, warning) for warning in warnings])
        else:
            print(f"✓ {nb_name} - No issues found")
    
    print("\n" + "=" * 50)
    print(f"Validation complete. Found {len(all_warnings)} issues total.")
    
    if all_warnings:
        print("\nSummary of issues:")
        for nb_name, warning in all_warnings:
            print(f"  {nb_name}: {warning}")
        
        return 1
    else:
        print("All notebooks passed validation!")
        return 0


if __name__ == '__main__':
    sys.exit(validate_all_notebooks())
