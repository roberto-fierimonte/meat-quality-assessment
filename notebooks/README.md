# Notebooks

This folder contains the notebooks that we use to experiment with this project.

## Overview

TODO

## Setup

In order to use these notebooks with the python virtual environment created by poetry follow the following steps:
1. Activate the poetry environment: `poetry shell`
2. Create a new Ipython kernel: `poetry run python -m ipykernel install --user --name="meat-quality-assessment"`
3. Wait 2 / 3 minutes and then select the newly available kernel in Jupyter notebook. This will make sure that all the required packages are installed


All the notebooks in this repository have their output stripped out to avoid pushing large files to the repository. Just re-run the notebooks to see their outputs.

## Notebooks

We have different notebooks corresponding to the different phases in the development of the project, covering from initial EDA to training and predicting. Below there is a short description of each notebook in this folder:

| Name        | Description                                               |
| :---------- |:--------------------------------------------------------- |
| 1-eda.ipynb | Contains the Exploratory Data Analysis on the input data. |
