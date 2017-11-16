"""
Plotting utilities for wgd
Arthur Zwaenepoel - 2017
"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


def plot_selection(dists, output_file=None, alphas=None, ks_range=(0.1, 5), offset=5, title='Species genus', **kwargs):
    """
    Plot a panel from the `all.csv` output from the Ks analysis.

    :param dists: distribution(s), if multiple provide as list
    :param alphas: alpha values for the different distributions (will assign automatically if not provided)
    :param ks_range: Ks range to include for plotting
    :param offset: offset of axis
    :param title: panel title
    :param kwargs: keyword arguments for :py:func:`matplotlib.pyplot.hist`
    :return: :py:class:`matplotlib.pyplot.Figure` object
    """
    fig = plt.figure(figsize=(12, 12))

    if type(dists) != list:
        dists = [dists]
        alphas = [alphas]

    if not alphas or not alphas[0]:
        alphas = list(np.linspace(0.2, 1, len(dists)))

    for i in range(len(dists)):
        dists[i] = dists[i][dists[i]['Ks'] > ks_range[0]]
        dists[i] = dists[i][dists[i]['Ks'] < ks_range[1]]

    # ks
    ax = fig.add_subplot(221)
    # get the bin edges
    bins = np.histogram(np.hstack(tuple([dist['Ks'] for dist in dists])), bins=40)[1]
    for i in range(len(dists)):
        ax.hist(dists[i]['Ks'], bins, alpha=alphas[i], color='black', rwidth=0.8,
                weights=dists[i]['WeightOutliersIncluded'], **kwargs)
    sns.despine(offset=offset, trim=True)
    ax.set_xlabel('$K_S$')

    # ka
    ax = fig.add_subplot(222)
    # get the bin edges
    bins = np.histogram(np.hstack(tuple([dist['Ka'] for dist in dists])), bins=40)[1]
    for i in range(len(dists)):
        ax.hist(dists[i]['Ka'], bins, alpha=alphas[i], color='black', rwidth=0.8,
                weights=dists[i]['WeightOutliersIncluded'], **kwargs)
    sns.despine(offset=offset, trim=True)
    ax.set_xlabel('$K_A$')

    # log(ka)
    ax = fig.add_subplot(223)
    # get the bin edges
    bins = np.histogram(np.hstack(tuple([np.log(dist['Ka']) for dist in dists])), bins=40)[1]
    for i in range(len(dists)):
        ax.hist(np.log(dists[i]['Ka']), bins, alpha=alphas[i], color='black', rwidth=0.8,
                weights=dists[i]['WeightOutliersIncluded'], **kwargs)
    sns.despine(offset=offset, trim=True)
    ax.set_xlabel('$ln(K_A)$')

    # log(w)
    ax = fig.add_subplot(224)
    # get the bin edges
    bins = np.histogram(np.hstack(tuple([np.log(dist['Omega']) for dist in dists])), bins=40)[1]
    for i in range(len(dists)):
        ax.hist(np.log(dists[i]['Omega']), bins, alpha=alphas[i], color='black', rwidth=0.8,
                weights=dists[i]['WeightOutliersIncluded'], **kwargs)
    sns.despine(offset=offset, trim=True)
    ax.set_xlabel('$ln(\omega)$')
    fig.suptitle(title)

    if output_file:
        fig.savefig(output_file, dpi=300, bbox_inches='tight')

    return fig


def syntenic_dotplot(df, output_file=None):
    """
    Syntenic dotplot function
    """
    genomic_elements = {x: 0 for x in list(set(df['list_x']) | set(df['list_y'])) if type(x) == str}

    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111)

    previous = 0
    for key in sorted(genomic_elements.keys()):
        length = max(list(df[df['list_x'] == key]['end_x']) + list(df[df['list_y'] == key]['end_y']))
        genomic_elements[key] = previous
        previous += length

    x = [genomic_elements[key] for key in sorted(genomic_elements.keys())] + [previous]
    ax.vlines(ymin=0, ymax=previous, x=x, linestyles='dotted', alpha=0.2)
    ax.hlines(xmin=0, xmax=previous, y=x, linestyles='dotted', alpha=0.2)
    ax.plot(x, x, color='k', alpha=0.2)
    ax.set_xticks(x)
    ax.set_yticks(x)
    ax.set_xticklabels(x)
    ax.set_yticklabels(x)

    for i in range(len(df)):
        row = df.iloc[i]
        list_x, list_y = row['list_x'], row['list_y']
        if type(list_x) != float:
            curr_list_x = list_x
        x = [genomic_elements[curr_list_x]+x for x in [row['begin_x'], row['end_x']]]
        y = [genomic_elements[list_y]+x for x in [row['begin_y'], row['end_y']]]
        ax.plot(x, y, color='k', alpha=0.5)
        ax.plot(y,x, color='k', alpha=0.5)

    sns.despine(offset=5, trim=True)

    if output_file:
        fig.savefig(output_file, dpi=200, bbox_inches='tight')

    else:
        return fig
