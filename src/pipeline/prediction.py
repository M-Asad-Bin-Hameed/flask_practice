from src.components.logger import logger
from src.utils import read_yaml_file, save_model
import pandas as pd
from src.components.data_ingestion import DataIngestor

class PredictionPipeline:
    def __init__(self, data_config_file_path) -> None:
        self.data_config_file_path = data_config_file_path
        self.data_config_file = read_yaml_file(self.data_config_file_path)
