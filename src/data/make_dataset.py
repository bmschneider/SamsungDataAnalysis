import requests
import zipfile
import io
import os
from pathlib import Path

uci_har_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00240/UCI%20HAR%20Dataset.zip"


def load_har_data_from_repo(fileout='.'):
    """Loads the UCI HAR data, and gets from repo if not there."""

    req = requests.get(uci_har_url)
    zfile = zipfile.ZipFile(io.BytesIO(req.content))
    zfile.extractall(fileout)
    return


def load_feature_data():
    """Load the feature data into `pandas.DataFrame`."""

    local_uci_har_path = Path('data/raw/UCI HAR Dataset')
    feature_name_df = pd.read_csv(local_uci_har_path / 'features.txt', sep='\s+', names=['id', 'name'])
    feature_name_df['unique_name'] = feature_name_df.apply(lambda x: x['name'] + '_' + str(x.id), axis=1)
    feature_names = feature_name_df.unique_name.tolist()

    path = local_uci_har_path / 'train'

    return pd.concat([
        pd.read_csv(path / 'subject_train.txt', sep='\s+', names=['subject_id']),
        pd.read_csv(path / 'X_train.txt', sep='\s+', names=feature_names),
        pd.read_csv(path / 'y_train.txt', sep='\s+', names=['activity_id'])
    ], axis=1)
