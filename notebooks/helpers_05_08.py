
"""
Helper functions for Decision Trees and Random Forests notebook.

This module provides visualization utilities for decision tree classifiers
used in the Python Data Science Handbook.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from ipywidgets import interact

# Set high DPI for better quality plots
plt.rcParams['figure.dpi'] = 600


def visualize_tree(estimator, X, y, boundaries=True,
                   xlim=None, ylim=None, ax=None):
    """
    Visualize a decision tree classifier with decision boundaries.
    
    Parameters
    ----------
    estimator : sklearn.tree.DecisionTreeClassifier
        The decision tree classifier to visualize
    X : array-like, shape (n_samples, 2)
        Training data features (must be 2D for visualization)
    y : array-like, shape (n_samples,)
        Training data labels
    boundaries : bool, default=True
        Whether to plot decision boundaries
    xlim : tuple, optional
        x-axis limits for the plot
    ylim : tuple, optional
        y-axis limits for the plot
    ax : matplotlib.axes.Axes, optional
        Axes object to plot on
        
    Returns
    -------
    None
        Creates a visualization plot
    """
    ax = ax or plt.gca()
    
    # Plot the training points
    ax.scatter(X[:, 0], X[:, 1], c=y, s=30, cmap='viridis',
               clim=(y.min(), y.max()), zorder=3)
    ax.axis('tight')
    ax.axis('off')
    if xlim is None:
        xlim = ax.get_xlim()
    if ylim is None:
        ylim = ax.get_ylim()
    
    # fit the estimator
    estimator.fit(X, y)
    xx, yy = np.meshgrid(np.linspace(*xlim, num=200),
                         np.linspace(*ylim, num=200))
    Z = estimator.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    n_classes = len(np.unique(y))
    Z = Z.reshape(xx.shape)
    contours = ax.contourf(xx, yy, Z, alpha=0.3,
                           levels=np.arange(n_classes + 1) - 0.5,
                           cmap='viridis', zorder=1)

    ax.set(xlim=xlim, ylim=ylim)
    
    # Plot the decision boundaries
    def plot_boundaries(i, xlim, ylim):
        if i >= 0:
            tree = estimator.tree_
        
            if tree.feature[i] == 0:
                ax.plot([tree.threshold[i], tree.threshold[i]], ylim, '-k', zorder=2)
                plot_boundaries(tree.children_left[i],
                                [xlim[0], tree.threshold[i]], ylim)
                plot_boundaries(tree.children_right[i],
                                [tree.threshold[i], xlim[1]], ylim)
        
            elif tree.feature[i] == 1:
                ax.plot(xlim, [tree.threshold[i], tree.threshold[i]], '-k', zorder=2)
                plot_boundaries(tree.children_left[i], xlim,
                                [ylim[0], tree.threshold[i]])
                plot_boundaries(tree.children_right[i], xlim,
                                [tree.threshold[i], ylim[1]])
            
    if boundaries:
        plot_boundaries(0, xlim, ylim)


def plot_tree_interactive(X, y):
    """
    Create an interactive decision tree visualization.
    
    Parameters
    ----------
    X : array-like, shape (n_samples, 2)
        Training data features
    y : array-like, shape (n_samples,)
        Training data labels
        
    Returns
    -------
    ipywidgets.interactive
        Interactive widget for controlling tree depth
    """
    def interactive_tree(depth=5):
        clf = DecisionTreeClassifier(max_depth=depth, random_state=0)
        visualize_tree(clf, X, y)

    return interact(interactive_tree, depth=(1, 5))


def randomized_tree_interactive(X, y):
    """
    Create an interactive visualization of randomized decision trees.
    
    Parameters
    ----------
    X : array-like, shape (n_samples, 2)
        Training data features
    y : array-like, shape (n_samples,)
        Training data labels
        
    Returns
    -------
    None
        Creates an interactive visualization
    """
    N = int(0.75 * X.shape[0])
    
    xlim = (X[:, 0].min(), X[:, 0].max())
    ylim = (X[:, 1].min(), X[:, 1].max())
    
    def fit_randomized_tree(random_state=0):
        clf = DecisionTreeClassifier(max_depth=15)
        i = np.arange(len(y))
        rng = np.random.RandomState(random_state)
        rng.shuffle(i)
        visualize_tree(clf, X[i[:N]], y[i[:N]], boundaries=False,
                       xlim=xlim, ylim=ylim)
    
    interact(fit_randomized_tree, random_state=(0, 100));
