import pandas as pd
from sklearn.model_selection import train_test_split
from src.components.logger import logger
from src.utils import read_yaml_file

class DataTransformer:
    def __init__(self, data_config_file_path, data) -> None:
        logger.info("Initializing data ingestion class")
        self.config_file_path = data_config_file_path
        self.config_file = read_yaml_file(self.config_file_path)
        self.config_file = self.config_file['data_transformation']
        self.data = data
        self.features = None
        self.target = None
    

    def transform_data(self):

        self.split_features_and_target()

        return self.perform_train_test_spit()
    def split_features_and_target(self):
        self.features = self.data.drop(columns=self.config_file['target'])
        self.target = self.data[self.config_file['target']]
        

    def perform_train_test_spit(self):
        X_train, X_test, y_train, y_test = \
            train_test_split(self.features,
                             self.target,
                             test_size=float(self.config_file['test_size']))
        return X_train, X_test, y_train, y_test

