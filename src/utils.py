import pickle
import os
import yaml
import pandas as pd
from src.components.logger import logger

def read_yaml_file(yaml_file):
    logger.info('Reading config file')
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    return data


def save_model(best_model, model_name):
    logger.info('Saving best model')

    output_dir = \
        os.path.join('artifacts/models/', f'{model_name.replace(" ", "_")}.pkl')
    with open(output_dir, 'wb') as file:
        pickle.dump(best_model, file)

def load_model():
    logger.info('Trying to load model')
    directory_path = 'artifacts/models'
    models = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.pkl'):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'rb') as file:
                model = pickle.load(file)
                models[filename.replace('.pkl','')] = model
            logger.info(f"Loaded model {filename.replace('.pkl','')}")
    return models

def get_data_details_for_prediction(data_path):
    data_configs = read_yaml_file('configs/data_config.yaml')
    data_type = data_configs['data_ingestion']['type']
    categorical_columns = \
        data_configs['data_ingestion'][data_type]['categorical_columns']
    logger.info('Called data details function')
    df = pd.read_csv(data_path)

    column_info = []
    for column_name, dtype in df.dtypes.items():
        if column_name != data_configs['data_transformation']['target']:
            if column_name in categorical_columns:
                field_type = 'select'
                unique_values = df[column_name].unique().tolist()
            elif pd.api.types.is_numeric_dtype(dtype):
                field_type = 'number'
            elif pd.api.types.is_string_dtype(dtype):
                field_type = 'text'
            else:
                field_type = 'text'
            
            column_info.append(
                (column_name,
                field_type,
                unique_values if field_type == 'select' else None)
                )
    
    return column_info