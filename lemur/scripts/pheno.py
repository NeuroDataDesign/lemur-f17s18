
# coding: utf-8

# In[ ]:


# Outside imports
import pandas as pd
import numpy as np
import os


# In[ ]:


# Load the lemur library
import sys
sys.path.append(".")
import lemur.datasets as lds
import lemur.metrics as lms
import lemur.plotters as lpl
import lemur.embedders as leb

# Create a lemur dataset based on the phenotypic data
CDS = lds.CSVDataSet("data/pheno/hbn_cleaned.csv",
                     name = "HBN Phenotypic")
metadata = CDS.saveMetaData("data/pheno/metadata.json")
CDS.imputeColumns("mean")
DM = lds.DistanceMatrix(CDS, lms.VectorDifferenceNorm)

# Create an embedded distance matrix object under MDS
MDSEmbedder = leb.MDSEmbedder(num_components=10)
HBN_Embedded = MDSEmbedder.embed(DM)


# In[ ]:


BASE = "data"
out_base = os.path.join(BASE, "pheno_derivatives")
out_emb_base = os.path.join(BASE, "pheno_embedded_deriatives")
os.makedirs(out_base + "/agg", exist_ok=True)
os.makedirs(out_emb_base + "/agg", exist_ok=True)


# In[ ]:


lpl.Heatmap(CDS, mode="savediv", base_path=out_base).plot()
lpl.Heatmap(HBN_Embedded, mode="savediv", base_path=out_emb_base).plot()


# In[ ]:


lpl.LocationLines(CDS, mode="savediv", base_path = out_base).plot()
lpl.LocationLines(HBN_Embedded, mode="savediv", base_path = out_emb_base).plot()


# In[ ]:


lpl.LocationHeatmap(CDS, mode="savediv", base_path=out_base).plot()
lpl.LocationHeatmap(HBN_Embedded, mode="savediv", base_path=out_emb_base).plot()


# In[ ]:


lpl.HistogramHeatmap(CDS, mode="savediv", base_path=out_base).plot()
lpl.HistogramHeatmap(HBN_Embedded, mode="savediv", base_path=out_emb_base).plot()


# In[ ]:


#lpl.CorrelationMatrix(CDS).plot()
#lpl.CorrelationMatrix(HBN_Embedded).plot()
#lpl.CorrelationMatrix(CDS, mode="savediv", base_path=out_base).plot()
#lpl.CorrelationMatrix(HBN_Embedded, mode="savediv", base_path=out_base).plot()


# In[ ]:


lpl.ScreePlotter(CDS, mode="savediv", base_path=out_base).plot()
lpl.ScreePlotter(HBN_Embedded, mode="savediv", base_path=out_emb_base).plot()


# In[ ]:


lpl.EigenvectorHeatmap(CDS, mode="savediv", base_path=out_base).plot()
lpl.EigenvectorHeatmap(HBN_Embedded, mode="savediv", base_path=out_base).plot()


# In[ ]:


lpl.HGMMPairsPlot(HBN_Embedded, mode="savediv", base_path=out_emb_base).plot(level=1)


# In[ ]:


lpl.HGMMClusterMeansDendrogram(HBN_Embedded, mode="savediv", base_path=out_emb_base).plot(level=1)


# In[ ]:


lpl.HGMMStackedClusterMeansHeatmap(HBN_Embedded, mode="savediv", base_path=out_emb_base).plot(level=4)


# In[ ]:


lpl.HGMMClusterMeansLevelHeatmap(HBN_Embedded, mode="savediv", base_path=out_emb_base).plot(level=4)


# In[ ]:


lpl.HGMMClusterMeansLevelLines(HBN_Embedded, mode="savediv", base_path=out_emb_base).plot(level=4)

