import os
import pandas as pd
from src.components.logger import logger
from src.utils import read_yaml_file


class DataIngestor:
    def __init__(self, data_config_file_path) -> None:
        logger.info("Initializing data ingestion class")
        self.config_file_path = data_config_file_path
        self.config_file = read_yaml_file(self.config_file_path)
        self.config_file = self.config_file['data_ingestion']
        self.raw_data = self.ingest_data()

    def ingest_data(self):
        logger.info(f'Ingesting Data of type {self.config_file["type"]}')
        if self.config_file['type'] == 'sklearn_internal':
            if self.config_file['sklearn_internal']['name']=='breast_cancer':
                from sklearn.datasets import load_breast_cancer
                data = load_breast_cancer()
                df = pd.DataFrame(data.data,columns=data.feature_names)
                df['target'] = data.target
            else:
                logger.error("Unsupported sklearn internal dataset for ingestion")
                df = None

        elif self.config_file['type'] == 'csv':
            df = pd.read_csv(self.config_file['csv']['location'])
        else:
            logger.error("Unsupported data type for ingestion")
            df = None
        if df is not None:
            sample_df = df.sample(n=1)
            csv_file = os.path.join('artifacts', 'sample_data.csv')
            sample_df.to_csv(csv_file, index=False)
            logger.success("Sample data written to artifacts folder")
        return df
