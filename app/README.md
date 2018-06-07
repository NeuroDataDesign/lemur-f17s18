 # Lemur's Automatic Visualization Application (LAVA)

**Hello researchers and datascientists alike!** Welcome to LAVA, a web-application that allows you to investigate multimodal datasets and **look at your data** before you move into deeper analyses.

### What is LAVA?

Our mission with LAVA is to provide a breadth of data visualizations with some level of depth to figure out how to gear more in-depth analyses. To do so, we provide visualizations of raw data, data transformed with multi-dimensional scaling, data that has been run through adaptive clustering algorithms (Adaptive KMeans or Hierarchial Gaussian Mixture Models), and one-to-one plots for EEG data.

#### List of Provided Visualizations:

Visit [our website](https://neurodatadesign.github.io/lemur/) to see images representing some of these different plots.

| Raw Data Plots         | Multi Dimensional Scaling Plots        | Clustering Plots              | EEG One-to-One Plots |
| ---------------------- | -------------------------------------- | ----------------------------- | -------------------- |
| Correlation Matrix     | Correlation Matrix                     | Cluster Means Dendogram       | Connected Scatter    |
| Heatmap                | Heatmap                                | Cluster Means Level Heatmap   | Sparkline            |
| Eigenvector Heatmap    | Eigenvector Heatmap                    | Cluster Means Level Lines     | Spatial Periodogram  |
| Histogram Heatmap      | Histogram Heatmap                      | Pairs Plot                    | Spatial Time Series  |
| Location Heatmap       | Location Heatmap                       | Stacked Cluster Means Heatmap |                      |
| Location Lines         | Location Lines                         |                               |                      |
| Scree Plot             | Scree Plot                             |                               |                      |


### Installing and Running the Application

LAVA requires installation of both [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/).

Clone our git repository:

`git clone https://github.com/NeuroDataDesign/lemur.git`

Add your AWS Credentials to the app/dir directory:

`cp path/to/your/credentials ./app/credentials/credentials`

Make sure your credentials are saved in the format used as a configuration file stored in the .aws folder:

``` \[default\]
aws_access_key_id = XXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXX
region = XXXXXXXXX
```
Go to our app folder:

`cd app`
`docker-compose up`

### Structuring Data