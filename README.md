# Samsung Data Analysis Project

An analysis of smartphone sensor data.

## Setting up the project

1. Start the container with `docker-compose up`.
1. Open the `1 - EDA.ipynb` file and run all cells.
1. Open the resulting report in `reports`

## Contents

Organized according to the [cookiecutter-datascience](https://drivendata.github.io/cookiecutter-data-science/) convention (folders are created during project setup).
* `config/start.py`: Jupyterlab config file.
* `data`: Landing point for data, broken up into `raw`, `interim`, and `processed`.
* `references/CodeBook.md`: description of the output data and transformations performed.
* `reports`: Landing point for reports.
* `notebooks/1 - EDA.ipynb`: Loading data and generating EDA report.
* `src`: python app for utilities needed.
* `requirements.txt`: Python requirements.
* `Dockerfile`: Environment build, including Jupyter config process.
* `docker-compose.yml`: Just adds project root folder as volume in the app.

## Data source
[UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphones)
