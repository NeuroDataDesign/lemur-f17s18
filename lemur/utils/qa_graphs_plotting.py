# qa_graphs_plotting.py
# Created by Greg Kiar on 2016-09-19.
# Email: gkiar@jhu.edu
# Edited by Coleman Zhang

from argparse import ArgumentParser
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot, plot
from lemurs.utils import plotly_helper as pp
import pickle
import numpy as np
import os

def make_panel_plot(statsDict, outf, dataset=None, atlas = None, minimal=True, 
                    log=True, hemispheres=True, modality='dwi'):

    """
    Given a dictionary of statistics generated by qa_graphs.compute_metrics(), 
    output an html file of plotly visualization.
    Required parameters:
        statsDict:
            - dictionary of statistics generated by qa_graphs.compute_metrics()
        outf:
            - The name of the generated plotly html file
    Optional parameters:
        atlas:
            - Name of atlas of interest as it appears in the directory titles
    """    

    dictKeys = list(statsDict.keys())
    dictKeys = sorted(dictKeys, key = str)
    
    if modality == 'dwi':
        modtit = "DWI"
        order = [0, 1, 2, 5, 4, 3, 6, 7]
        dictKeys = [dictKeys[o] for o in order]
        labs = ['Betweenness Centrality', 'Clustering Coefficient', 'Degree',
                'Locality Statistic-1', 'Eigenvalue', 'Edge Weight',
                'Number of Non-zeros', 'Mean Connectome']
        
    else:
        modtit = "fMRI"
        order = [0, 1, 2, 6, 4, 3, 5, 7]
        dictKeys = [dictKeys[o] for o in order]
        labs = ['Betweenness Centrality', 'Clustering Coefficient', 'Degree',
                'Average Path Length', 'Locality Statistic-1', 'Eigenvalue',
                'Number of Non-zeros', 'Mean Connectome']
    traces = list(())
    
    for idx, curr in enumerate(dictKeys):
        dat = statsDict[dictKeys[idx]]
        if dictKeys[idx] == 'number_non_zeros':
            fig = pp.plot_rugdensity(dat.values())
        elif dictKeys[idx] == 'edge_weight':
            edges = np.max([len(dat[i]) for i in dat.keys()])
            fig = pp.plot_series(dat.values(), sort=True)
        elif dictKeys[idx] == 'degree_distribution':
            fig = pp.plot_degrees(dat, hemi=hemispheres)
            if hemispheres:
                maxdat = np.max([np.max(dat[key][k]) 
                                 for key in dat.keys()
                                 for k in dat[key]])
                anno = [dict(x=dims/3,
                             y=4*float(maxdat/7),
                             xref='x3',
                             yref='y3',
                             text='ipsilateral',
                             showarrow=False,
                             font=dict(color='rgba(0.0,0.0,0.0,0.6)',
                                       size=14)),
                        dict(x=dims/3,
                             y=3.7*float(maxdat/7),
                             xref='x3',
                             yref='y3',
                             text='contralateral',
                             showarrow=False,
                             font=dict(color='rgba(0.11,0.62,0.47,0.6)',
                                       size=14))]
        elif dictKeys[idx] == 'study_mean_connectome':
            if log:
                dat = np.log10(dat+1)
            fig = pp.plot_heatmap(dat, name=labs[idx])
        else:
            dims = len(dat.values()[0])
            fig = pp.plot_series(dat.values())
        traces += [fig_to_trace(fig)]

    multi = pp.traces_to_panels(traces)
    for idx, curr, in enumerate(dictKeys):
        key = 'axis%d' % (idx+1)
        d = multi.layout['x'+key]['domain']
        multi.layout['x'+key]['domain'] = [d[0], d[1]-0.0125]
        multi.layout['x'+key]['zeroline'] = False
        multi.layout['y'+key]['zeroline'] = False
        multi.layout['y'+key]['title'] = ''
        multi.layout['x'+key]['title'] = 'Node'
        multi.layout['x'+key]['nticks'] = 3
        multi.layout['y'+key]['nticks'] = 3
        if (idx in [0, 1, 2, 3, 4, 5] and modality == 'func') or (idx in [0, 1, 2, 3, 4, 5] and modality == 'dwi'):
            multi.layout['x'+key]['range'] = [1, dims]
            multi.layout['x'+key]['tickvals'] = [1, dims/2, dims]
            if idx in [2]:
                if hemispheres:
                    multi.layout['annotations'] = anno
            elif log:
                multi.layout['y'+key]['type'] = 'log'
                multi.layout['y'+key]['title'] += 'log'
        if idx in [5] and modality == 'dwi':
            multi.layout['x'+key]['range'] = [1, edges]
            multi.layout['x'+key]['tickvals'] = [1, edges/2, edges]
            multi.layout['x'+key]['title'] = 'Edge'
        if (idx in [4] and modality == 'dwi') or (idx in [5] and modality == 'func'):
            multi.layout['x'+key]['range'] = [1, dims]
            multi.layout['x'+key]['tickvals'] = [1, dims/2, dims]
            multi.layout['x'+key]['title'] = 'Dimension'
        multi.layout['y'+key]['title'] += labs[idx]
        if (idx in [6]):
            multi.layout['y'+key]['title'] = 'Relative Probability'
            multi.layout['x'+key]['title'] = labs[idx]
        if idx in [7]:
            multi.layout['y'+key]['title'] = None
            multi.layout['x'+key]['title'] = labs[idx]
            multi.layout['y'+key]['autorange'] = 'reversed'
            multi.layout['x'+key]['tickvals'] = [0, dims/2-1, dims-1]
            multi.layout['y'+key]['tickvals'] = [0, dims/2-1, dims-1]
            multi.layout['x'+key]['ticktext'] = [1, dims/2, dims]
            multi.layout['y'+key]['ticktext'] = [1, dims/2, dims]
            if log:
                multi.layout['x'+key]['title'] += ' (log10)'
    if dataset is not None and atlas is not None:
        if atlas == 'desikan':
            atlas = atlas.capitalize()
        tit = "{} Dataset ({} parcellation), {} Group Analysis".format(dataset,
                atlas, modtit)
    else:
        tit = "{} Group Analysis".format(modtit)
    multi.layout['title'] = tit
    # iplot(multi, validate=False)

    if minimal:
        locs = [idx for idx, d in enumerate(multi.data) if d['yaxis'] == 'y8']
        for l in locs:
            multi.data[l] = {}
        multi.layout['x'+key]['title'] = ''
        multi.layout['y'+key]['title'] = ''
        multi = pp.panel_invisible(multi, 8)

    plot(multi, validate=False, filename=outf+'.html')