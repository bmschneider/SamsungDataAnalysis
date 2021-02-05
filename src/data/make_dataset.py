import requests
import zipfile
import io
import os
from pathlib import Path
import pandas as pd

uci_har_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00240/UCI%20HAR%20Dataset.zip"


def load_har_data_from_repo(fileout='.'):
    """Loads the UCI HAR data, and gets from repo if not there."""

    if os.path.exists('data/raw/UCI HAR Dataset'):
        print('Data appears to be already obtained.')
        return

    if not os.path.exists('data'): os.mkdir('data')
    if not os.path.exists('data/raw'): os.mkdir('data/raw')
    req = requests.get(uci_har_url)
    zfile = zipfile.ZipFile(io.BytesIO(req.content))
    zfile.extractall(fileout)
    return


def load_raw_signal(signal_name, path, file):
    """Load a single signal from `path` and `file`."""

    dataset_path = path / 'Inertial Signals'
    windows = pd.read_csv(dataset_path / file, sep='\s+', header=None)
    signal = windows \
        .iloc[:, :64] \
        .reset_index() \
        .melt(id_vars='index', value_name=signal_name) \
        .sort_values(by=['index', 'variable']) \
        .reset_index(drop=True)
    signal['time_exp'] = signal['variable']*0.02

    return signal[['index', 'time_exp', signal_name]]


def load_raw_data(dataset='train'):
    """Load the windowed raw data into `pandas.DataFrame` for the `dataset`."""

    if not os.path.exists('data/interim'): os.mkdir('data/interim')
    if os.path.exists('data/interim/raw_df.csv'):
        return pd.read_csv('data/interim/raw_df.csv')
    local_uci_har_path = Path('data/raw/UCI HAR Dataset')

    path = local_uci_har_path / dataset

    subjects = pd.read_csv(path / f'subject_{dataset}.txt',
                           sep='\s+',
                           names=['subject_id']) \
        .reset_index()
    labels = pd.read_csv(path / f'y_{dataset}.txt',
                         sep='\s+',
                         names=['activity_id']) \
        .reset_index()

    signal_names = ['body_acc_x', 'body_acc_y', 'body_acc_z',
                    'body_gyro_x', 'body_gyro_y', 'body_gyro_z',
                    'total_acc_x', 'total_acc_y', 'total_acc_z']

    sensors = load_raw_signal(signal_names[0],
                              path,
                              f'{signal_names[0]}_{dataset}.txt')
    for s in signal_names[1:]:
        sensors = sensors.merge(load_raw_signal(s, path, f'{s}_{dataset}.txt'))

    full_dataset = subjects.merge(sensors).merge(labels).drop('index', axis=1)
    full_dataset.to_csv('data/interim/raw_df.csv', index=False)

    return full_dataset


def load_feature_names(path):
    """Loads feature names, adding column index for duplicated names."""

    feature_name_df = pd.read_csv(path / 'features.txt',
                                  sep='\s+',
                                  names=['id', 'name'])
    feature_name_df = feature_name_df.merge(
        feature_name_df.groupby(by='name').size().reset_index()
    ).rename(columns={0: 'count'})
    feature_name_df['unique_name'] = feature_name_df['name']
    feature_name_df.loc[feature_name_df['count'] > 1, 'unique_name'] = feature_name_df \
        .loc[feature_name_df['count'] > 1, :] \
        .apply(lambda x: x['name'] + '_' + str(x.id), axis=1)
    return feature_name_df.unique_name.tolist()


def load_feature_data(dataset='train'):
    """Load the feature data into `pandas.DataFrame`."""

    if not os.path.exists('data/interim'): os.mkdir('data/interim')
    if os.path.exists('data/interim/feature_df.csv'):
        return pd.read_csv('data/interim/feature_df.csv')

    local_uci_har_path = Path('data/raw/UCI HAR Dataset')
    feature_names = load_feature_names(local_uci_har_path)

    path = local_uci_har_path / dataset

    full_dataset = pd.concat([
        pd.read_csv(path / f'subject_{dataset}.txt', sep='\s+',
                    names=['subject_id']),
        pd.read_csv(path / f'X_{dataset}.txt', sep='\s+', names=feature_names),
        pd.read_csv(path / f'y_{dataset}.txt', sep='\s+', names=['activity_id'])
    ], axis=1)

    full_dataset.to_csv('data/interim', index=False)

    return full_dataset
