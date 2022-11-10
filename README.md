<div id="top"></div>

<!-- PROJECT LOGO -->
<br>
<div align="center">
  <a href="https://bitbucket.org/robertofierimonte/meat-quality-assessment/">
    <img src="docs/images/logo.jpg" alt="Logo" height="350">
  </a>

<h2 align="center">Meat Quality Assessment</h2>
  <p>Deep Learning model to assess the quality of red meat based on sample photos.<br>
  Author: <a href="mailto:roberto.fierimonte@gmail.com"><b>Roberto Fierimonte</b></a></p>
</div>

<!-- TABLE OF CONTENTS -->
 <h3 align="center">Table of Contents</h3>
 <ol>
 <li>
  <a href="#about-the-project">About the Project</a>
 </li>
 <li>
  <a href="#getting-started">Getting Started</a>
  <ul>
   <li><a href="#prerequisites">Prerequisites</a></li>
   <li><a href="#repo-structure">Repo structure</a></li>
   <li><a href="#local-setup">Local setup</a></li>
   <li><a href="#notebooks">Notebooks</a></li>
  </ul>
 </li>
 <li>
  <a href="#training-and-testing-the-model">Training and testing the model</a>
 </li>
</ol>

<!-- ABOUT THE PROJECT -->
## About the Project

Food waste is a big problem in our world.

The goal of this project is to build a Machine Learning model that predicts whether meat is fresh or spoiled and can therefore be consumed.

The dataset used in this project was originally built for this [research paper](https://ieeexplore.ieee.org/abstract/document/8946388) and subsequently made available on [Kaggle](https://www.kaggle.com/datasets/crowww/meat-quality-assessment-based-on-deep-learning).

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

### Prerequisites
- Python 3.9 (we are using version `3.9.7`)
- [poetry](https://python-poetry.org/) (we are using version `1.2.2`)
- [pre-commit](https://pre-commit.com/)
- [Docker](https://www.docker.com/)
- A [Kaggle](https://www.kaggle.com/) account

Since the dataset is hosted on Kaggle and not provided with the repository, it is not possible to run this code without having a Kaggle account.

### Repo structure

The repository is structured as follows:

```
meat-quality-assessment
├── containers
├── docs
├── data
├── model
├── notebooks
└── src
     ├── base
     ├── scripts
     └── serving_api
```

- The `containers` folder contains the Dockerfile used to build the image for the serving API
- The `docs` folder contains the images and additional documentation about the project
- The `data` folder is empty and it will be populated with the dataset after completing the local setup
- The `model` folder is empty and it will be populated with the serialised model files after running the training notebook
- The `notebooks` folder contains the notebooks for exploratory analysis over the data, as well as the training and testing of the model
- The `src` folder contains the source code for the project:
   - The `base` subfolder contains the code used for the exploratory analysis and the model
   - The `scripts` subfolder contains the script to download the dataset
   - The `serving_api` subfolder contains the code to run the serving API

### Local setup

In the repository, execute:

1. Install poetry if not available: `pip install poetry==1.2.2`
2. Install pre-commit if not available: `pip install pre-commit`
3. Install packages: `poetry install`
4. Install pre-commit hooks: `pre-commit install`
5. Follow these steps to download and set up a `kaggle.json` file with your Kaggle API token:
    1. Login into your Kaggle account
    2. Get into your account settings page
    3. Click on Create a new API token
    4. This will prompt you to download the `kaggle.json` file into your system
    5. Move the file into the root folder of the repository, and we will use it in the next step
6. Download the dataset by running `make download-data`
7. Follow the instructions in the `.env.example` to set up the necessary environment variables
8. Run `make help` to see all the options provided in the Makefile

### Notebooks

The project supports local usage and development by Jupyter Notebooks. Examples of the EDA, local training and local predictions on Notebooks are included in the [notebooks](notebooks/) folder.

See [Notebooks README](notebooks/README.md) for more information about how to use notebooks.

<p align="right">(<a href="#top">back to top</a>)</p>

## Training and testing the model

A trained model is not provided with this repository. To train the model please the [training notebook](notebooks/2-training.ipynb) end to end. That will save the model in the [model](model/) folder for it to be used to predict new images.

To test the trained model you have two options:
1. You can run the [prediction notebook](notebooks/3-predict.ipynb). This will make a batch prediction of a test set of images not used during training
2. You can use the REST API to provide an image file to the model to scored:
    * Run `make run-server` to run the REST API in a Docker container, or
    * Run `make run-server-local` to run the REST API through `gunicorn` on your machine (this solution does not work on Windows due to the limitations of `gunicorn`)
    * In a different shell window, run `make test-api image=<image-path>`, where `image_path` is the path of the image that you want to score. We provided an example image that can be scored by running `make test-api image=example.jpg`, however you can score any image by passing its path

<p align="right">(<a href="#top">back to top</a>)</p>
