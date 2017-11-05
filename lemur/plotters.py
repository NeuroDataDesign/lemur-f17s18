from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from ipywidgets import interact

class DistanceMatrixPlotter:

    def __init__(self, dm, primary_label = "resource_path"):
        self.dataset_name = dm.dataset.name
        self.dm = dm.getMatrix()
        self.label_name = primary_label
        self.label = dm.dataset.D[primary_label]
        self.metric_name = dm.metric.__name__


class DistanceMatrixHeatmap(DistanceMatrixPlotter):
    titlestring = "%s Distance Matrix Heatmap under %s metric"

    def plot(self):
        title = self.titlestring % (self.dataset_name, self.metric_name)
        xaxis = go.XAxis(
                title="data points",
                ticktext = self.label,
                ticks = "",
                showticklabels=False,
                mirror=True,
                tickvals = [i for i in range(len(self.label))])
        yaxis = go.YAxis(
                title="data points",
                ticktext = self.label,
                ticks = "",
                showticklabels=False,
                mirror=True,
                tickvals = [i for i in range(len(self.label))])
        layout = dict(title=title, xaxis=xaxis, yaxis=yaxis, width=600, height=600)
        trace = go.Heatmap(z = self.dm)
        data = [trace]
        fig = dict(data=data, layout=layout)
        iplot(fig)

class DistanceMatrixEigenvectorHeatmap(DistanceMatrixPlotter):
    titlestring = "%s Distance Matrix Eigenvector Heatmap under %s metric"

    def plot(self):
        title = self.titlestring % (self.dataset_name, self.metric_name)
        U, _, _ = np.linalg.svd(self.dm, full_matrices=False)
        xaxis = go.XAxis(
                title="eigenvectors",
                ticktext = ["Eigenvector %s"%i for i in range(1, len(self.label) + 1)],
                ticks = "",
                showticklabels=False,
                mirror=True,
                tickvals = [i for i in range(len(self.label))])
        yaxis = go.YAxis(
                title="eigenvector components",
                ticktext = ["Component %s"%i for i in range(1, len(self.label) + 1)],
                ticks = "",
                showticklabels=False,
                mirror=True,
                tickvals = [i for i in range(len(self.label))])
        layout = dict(title=title, xaxis=xaxis, yaxis=yaxis, width=600, height=600)
        trace = go.Heatmap(z = U)
        data = [trace]
        fig = dict(data=data, layout=layout)
        iplot(fig)

class DistanceMatrixScreePlotter(DistanceMatrixPlotter): 
    titlestring = "%s Distance Matrix Scree Plot under %s metric"

    def plot(self):
        title = self.titlestring % (self.dataset_name, self.metric_name)
        _, S, _ = np.linalg.svd(self.dm, full_matrices=False)
        y = S
        x = np.arange(1, len(S) + 1)
        sy = np.sum(y)
        cy = np.cumsum(y)
        xaxis = dict(
            title = 'Factors'
        )
        yaxis = dict(
            title = 'Proportion of Total Variance'
        )
        var = go.Scatter(mode = 'lines+markers',
                         x = x,
                         y = y / sy,
                         name = "Variance")
        cumvar = go.Scatter(mode = 'lines+markers',
                            x = x,
                            y = cy / sy,
                            name = "Cumulative Variance")
        data = [var, cumvar]
        layout = dict(title=title, xaxis=xaxis, yaxis=yaxis)
        fig = dict(data=data, layout=layout)
        iplot(fig)
    
class Embedding2DScatter(DistanceMatrixPlotter):
    titlestring = "%s 2D %s Embedding Scatter under %s metric"

    def plot(self, embedder):
        title = self.titlestring % (self.dataset_name, embedder.embedding_name, self.metric_name)
        emb = embedder.embed(self.dm)
        d = {
            'factor 1': emb[:, 0],
            'factor 2': emb[:, 1],
            self.label_name: self.label
        }
        D = pd.DataFrame(d)
        sns.lmplot('factor 1',
                   'factor 2',
                    data = D,
                    fit_reg = False,
                    hue=self.label_name)
        plt.title(title)
        plt.show()

class EmbeddingHeatmap(DistanceMatrixPlotter):
    titlestring = "%s %s Embedding Heatmap under %s metric"

    def plot(self, embedder):
        title = self.titlestring % (self.dataset_name, embedder.embedding_name, self.metric_name)
        emb = embedder.embed(self.dm).T
        xaxis = go.XAxis(
                title="data points",
                ticktext = self.label,
                ticks = "",
                showticklabels=False,
                mirror=True,
                tickvals = [i for i in range(len(self.label))])
        yaxis = go.YAxis(
                title="embedding dimensions",
                ticktext = ["factor %s"%i for i in range(1, len(self.label) + 1)],
                ticks = "",
                showticklabels=False,
                mirror=True,
                tickvals = [i for i in range(len(self.label))])
        layout = dict(title=title, xaxis=xaxis, yaxis=yaxis, width=600, height=600)
        trace = go.Heatmap(z = emb)
        data = [trace]
        fig = dict(data=data, layout=layout)
        iplot(fig)

class EmbeddingPairsPlotter(DistanceMatrixPlotter):
    titlestring = "%s %s Embedding Pairs Plot under %s metric"

    def plot(self, embedder):
        title = self.titlestring % (self.dataset_name, embedder.embedding_name, self.metric_name)
        emb = embedder.embed(self.dm)
        Pdf = pd.DataFrame(emb, columns = ["factor %s"%x for x in range(1, emb.shape[1] + 1)])
        Pdf[self.label_name] = self.label
        sns.pairplot(data=Pdf, hue=self.label_name, diag_kind="hist")
        plt.subplots_adjust(top=0.9)
        plt.suptitle(title)
        plt.show()

class EmbeddingParallelCoordinatePlotter(DistanceMatrixPlotter):
    titlestring = "%s %s Embedding Parallel Coordinate Plot under %s metric"

    def plot(self, embedder):
        title = self.titlestring % (self.dataset_name, embedder.embedding_name, self.metric_name)
        emb = embedder.embed(self.dm)
        D = emb.T
        d, n = D.shape
        D = D - np.min(D, axis=1).reshape(d, 1)
        D = D / np.max(D, axis=1).reshape(d, 1)
        unique_labels = np.unique(self.label)
        label_to_number = dict(zip(unique_labels, range(1, len(unique_labels) + 1)))
        dims = [dict(label = "factor %s"%(x + 1),
                values = D[x, :]) for x in range(embedder.num_components)]
        line = dict(color = [label_to_number[x] for x in self.label],
                    cmin = 0,
                    cmax = len(unique_labels),
                    colorscale = "Jet",
                    showscale=True,
                    colorbar = dict(tickmode = "array",
                                    ticktext = unique_labels,
                                    tickvals = [label_to_number[x] for x in unique_labels]))
        trace = go.Parcoords(line = line, dimensions = list(dims))
        data = [trace]
        layout = go.Layout(
            title=title
        )
        fig = dict(data = data, layout = layout)
        iplot(fig)

class DendrogramPlotter(DistanceMatrixPlotter):
    titlestring = "%s Dendrogram under %s metric"

    def plot(self):
        title = self.titlestring % (self.dataset_name, self.metric_name)
        observations = np.zeros([2, 2])
        unique_labels = np.unique(self.label)
        label_to_number = dict(zip(unique_labels, range(1, len(unique_labels) + 1)))
        number_labels = [label_to_number[l] for l in self.label]
        def distance_function(x):
            return self.dm[np.triu_indices(self.dm.shape[0], k=1)].flatten()

        dendro = ff.create_dendrogram(X = observations,
                                      distfun = distance_function,
                                      labels=number_labels)
        dendro.layout.update(dict(title=title))
        dendro.layout.xaxis.update(dict(ticktext=self.label,
                                        title=self.label_name,
                                        ticklen=2))
        dendro.layout.xaxis.tickfont.update(dict(size=8))
        dendro.layout.yaxis.update(dict(title=self.metric_name))
        dendro.layout.margin.update(dict(b = 100))
        iplot(dendro)
