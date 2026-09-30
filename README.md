# IMU-Motion: An IMU-Based Human Motion Dataset

A dataset and data-processing repository for human motion data collected using wearable inertial measurement units (IMUs) and a smartphone-based inertial sensor.

The repository provides the code used to load, preprocess, synchronize, trim, resample, and visualize the collected sensor data.

## Dataset

The dataset is publicly available through Zenodo:

**DOI:** [10.5281/zenodo.22902930](https://doi.org/10.5281/zenodo.22902930)

Please download the dataset from Zenodo before running the processing notebook.

After downloading the dataset, place the extracted `data` directory in the root of this repository:

```text
IMU-Motion/
├── data/
├── notebooks/
├── src/
├── config.yaml
├── requirements.txt
└── README.md

## Repository Structure

IMU-Motion/
│
├── data/
│   └── [Dataset downloaded from Zenodo]
│
├── notebooks/
│   ├── DataProcessing.ipynb
│
├── src/
│   ├── data_loader.py
│   ├── preprocess_data.py
│   └── visualisation.py
│
├── config.yaml
├── requirements.txt
├── LICENSE
└── README.md

1. notebooks/- Contains Jupyter notebooks used for data exploration and processing.
2. DataProcessing.ipynb — main notebook for processing and visualizing the dataset.
3. src/- Contains reusable Python functions used by the notebook.
4. data_loader.py — functions for loading sensor data.
5. preprocess_data.py — preprocessing, trimming, timestamp synchronization, and resampling functions.
6. visualisation.py — functions for plotting sensor signals and synchronization checkpoints.
7. config.yaml- Contains dataset paths, session definitions, sensor folder names, and file naming conventions.
8. requirements.txt- Contains the Python dependencies required to run the processing code.

## Dataset Structure from Zenodo

After downloading and extracting the dataset from Zenodo, the data is organized by subject and recording session.

data/
│
├── Subject_1_D/
│   ├── Session_1/
│   └── Session_2/
│
├── Subject_2_F/
│   ├── Session_1/
│   └── Session_2/
│
└── Subject_3_I/
    ├── Session_1/
    └── Session_2/

## Processing Pipeline

The main processing workflow is:

Raw Dataset
     │
     ├── Xsens IMU recordings
     │
     ├── Sensor Logger recordings
     │
     └── Step Logger events
     │
     ▼
Data Loading
     │
     ▼
Signal Trimming
     │
     ▼
Timestamp Processing
     │
     ▼
Xsens / Sensor Logger Synchronization
     │
     ▼
Sensor Logger Resampling
     │
     ▼
Processed Sensor Data
     │
     ▼
Visualization and Analysis

The processing functions are implemented in src/ and called from: notebooks/DataProcessing.ipynb

## Configuration

Dataset locations and processing-related file names are specified in: config.yaml

The configuration includes:

Dataset directory
Subject/session paths
Sensor Logger directories
Xsens directories
Processed-data directories
File naming conventions

Before running the notebook, make sure that the paths in config.yaml correspond to the location of the downloaded dataset.

## Installation

Clone the repository : 

git clone <repository-url>
cd IMU-Motion

Create and activate a Python environment, then install the required dependencies:

pip install -r requirements.txt

## Running the Processing Notebook

After downloading the dataset from Zenodo and placing it in the expected data/ directory:

1. Open the repository in VS Code or Jupyter.
2. Open: notebooks/DataProcessing.ipynb

3. Run the notebook cells sequentially.

The notebook uses the reusable functions in:
src/data_loader.py
src/preprocess_data.py
src/visualisation.py

