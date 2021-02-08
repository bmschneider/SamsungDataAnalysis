import requests
import zipfile
import io
import os
from pathlib import Path
import pandas as pd

uci_har_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00240/UCI%20HAR%20Dataset.zip"
local_uci_har_path = Path('data/raw/UCI HAR Dataset')

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


def load_subject_series(path, dataset='train'):
    """Load the subject series and determine time_exp."""

    subjects = pd.read_csv(path / f'subject_{dataset}.txt',
                           sep='\s+',
                           names=['subject_id']) \
        .reset_index()
    min_indices = subjects \
        .groupby(by='subject_id') \
        .min()['index'] \
        .reset_index() \
        .rename(columns={'index': 'min_index'})

    subjects_min = subjects.merge(min_indices)
    subjects_min['time_exp'] = \
        1.28*(subjects_min['index'] - subjects_min.min_index)

    return subjects_min[['index', 'subject_id', 'time_exp']]


def load_activity_names():
    """Load the activity names."""

    return pd.read_csv(local_uci_har_path / f'activity_labels.txt',
                       sep='\s+',
                       names=['activity_id', 'activity_name'])


def load_raw_signal(signal_name, path, file):
    """Load a single signal from `path` and `file`."""

    dataset_path = path / 'Inertial Signals'
    windows = pd.read_csv(dataset_path / file, sep='\s+', header=None)
    signal = windows \
        .iloc[:, :64] \
        .reset_index() \
        .melt(id_vars='index', value_name=signal_name, var_name='time_counter') \
        .sort_values(by=['index', 'time_counter']) \
        .reset_index(drop=True)
    signal['time_counter'] = signal.time_counter.astype(int)

    return signal[['index', 'time_counter', signal_name]]


def load_raw_data(dataset='train'):
    """Load the windowed raw data into `pandas.DataFrame` for the `dataset`."""

    if not os.path.exists('data/interim'): os.mkdir('data/interim')
    file_path = Path(f'data/interim/raw_{dataset}_df.csv')
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    local_uci_har_path = Path('data/raw/UCI HAR Dataset')

    path = local_uci_har_path / dataset

    subjects = load_subject_series(path, dataset)
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

    full_dataset = subjects \
        .merge(sensors) \
        .merge(labels)
    full_dataset['time_exp'] = full_dataset \
        .apply(
            lambda x: x.time_exp + x.time_counter*0.02,
            axis=1)
    final_col_set = ['subject_id', 'time_exp'] + signal_names + ['activity_id']
    full_dataset.loc[:, final_col_set] \
        .to_csv(file_path, index=False)
    return full_dataset.loc[:, final_col_set]


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

    data_interim_path = Path('data/interim')
    file_interim = data_interim_path / f'feature_{dataset}_df.csv'
    if not os.path.exists(data_interim_path): os.mkdir(data_interim_path)
    if os.path.exists(file_interim):
        return pd.read_csv(file_interim)

    local_uci_har_path = Path('data/raw/UCI HAR Dataset')
    feature_names = load_feature_names(local_uci_har_path)

    path = local_uci_har_path / dataset
    subjects = load_subject_series(path, dataset)

    full_dataset = pd.concat([
        subjects.drop('index', axis=1),
        pd.read_csv(path / f'X_{dataset}.txt', sep='\s+', names=feature_names),
        pd.read_csv(path / f'y_{dataset}.txt', sep='\s+', names=['activity_id'])
    ], axis=1)

    full_dataset.to_csv(file_interim, index=False)

    return full_dataset
