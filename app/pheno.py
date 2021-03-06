# Outside imports
import pandas as pd
import numpy as np
import os
import pickle as pkl


# Load the lemur library
import sys
sys.path.append("..")
import lemur.datasets as lds
import lemur.metrics as lms
import lemur.plotters as lpl
import lemur.clustering as lcl
import lemur.embedders as leb

def run_pheno(name):

    BASE = "data"
    # Create a lemur dataset based on the phenotypic data
    DATASET = os.path.split(os.path.split(name)[0])[1]
    root = os.path.join(BASE, DATASET, 'pheno')



    CDS = lds.CSVDataSet(name, name = DATASET)
    # metadata = CDS.saveMetaData(os.path.join("data", DATASET, "metadata.json"))
    CDS.imputeColumns("mean")
    DM = lds.DistanceMatrix(CDS, lms.VectorDifferenceNorm)

    # Set output paths for saved plots.
    with open(os.path.join(root, 'dm.pkl'), 'wb') as pkl_loc:
        pkl.dump(DM, pkl_loc)

    # Create an embedded distance matrix object under MDS
    MDSEmbedder = leb.MDSEmbedder(num_components=10)
    HBN_Embedded = MDSEmbedder.embed(DM)
    with open(os.path.join(root, 'embed_dm.pkl'), 'wb') as pkl_loc:
        pkl.dump(HBN_Embedded, pkl_loc)

    hgmm = lcl.HGMMClustering(HBN_Embedded, 4)
    hgmm.cluster()
    with open(os.path.join(root, 'hgmm_clust_dm.pkl'), 'wb') as pkl_loc:
        pkl.dump(hgmm, pkl_loc)

    clustered = lcl.AdaptiveKMeans(HBN_Embedded)
    clustered.cluster()
    with open(os.path.join(root, 'km_clust_dm.pkl'), 'wb') as pkl_loc:
        pkl.dump(clustered, pkl_loc)
