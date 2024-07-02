from src.components.logger import logger
from src.utils import read_yaml_file, load_model
import pandas as pd
import numpy as np
from src.components.data_ingestion import DataIngestor

class PredictionPipeline:
    def __init__(self, data_config_file_path) -> None:
        self.data_config_file_path = data_config_file_path
        self.data_config_file = read_yaml_file(self.data_config_file_path)
        self.models = load_model()

    def predict(self, data):
        output_list = list(data.values())
        input_array = np.array(output_list).reshape(1, -1)
        predictions = {}
        for k,v in self.models.items():
            predictions[k] = v.predict(input_array)[0]
        return self.format_output(predictions)

    def format_output(self, output):
        output_str = ''
        for k,v in output.items():
            output_str +=f"""
        {k} model predicted the value {v}
        """
        return output_str