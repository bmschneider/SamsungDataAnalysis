# Samsung Data Analysis Project

An analysis project of smartphone sensor data which demonstrates many techniques.

## Setting up the project

1. Start the container with `docker-compose up`.
1. Open the notebooks and run all cells in order.
1. Open the resulting report in `reports`

## Contents

Organized according to the [cookiecutter-datascience](https://drivendata.github.io/cookiecutter-data-science/) convention (folders are created during project setup).
* `config/start.py`: Jupyterlab config file.
* `data`: Landing point for data, broken up into `raw`, `interim`, and `processed`.
* `references/CodeBook.md`: description of the output data and transformations performed.
* `reports`: Landing point for reports.
* `notebooks`: Notebooks for analyses, numbered for convenience.
* `src`: python app for utilities needed.
* `requirements.txt`: Python requirements.
* `Dockerfile`: Environment build, including Jupyter configuration.
* `docker-compose.yml`: Just adds project root folder as volume in the app.

## Data source
[UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphones)
[UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/machine-learning-databases/00341/)
https://archive.ics.uci.edu/ml/machine-learning-databases/00341/HAPT%20Data%20Set.zip
