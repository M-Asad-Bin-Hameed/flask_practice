from src.components.logger import logger
from src.components.data_ingestion import DataIngestor
from src.components.data_transformation import DataTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from src.utils import read_yaml_file, save_model
import pandas as pd

class TrainingPipeline:
    def __init__(self, data_config_file_path) -> None:
        self.data_config_file_path = data_config_file_path
        self.data_config_file = read_yaml_file(self.data_config_file_path)

    def train(self,):
        data_ingestion_module = DataIngestor(self.data_config_file_path)
        data = data_ingestion_module.ingest_data()
        data_transformation_module = DataTransformer(self.data_config_file_path,data)
        self.X_train, self.X_test, self.y_train, self.y_test = \
            data_transformation_module.transform_data()
        if self.data_config_file['problem']['type'] == 'classification':
            best_model_name = self.perform_classification_training()
        elif self.data_config_file['problem']['type'] == 'regression':
            best_model_name = self.perform_regression_training()
        return best_model_name

    def perform_classification_training(self):
        models = {
            'LR': LogisticRegression(max_iter=5000),
            'SVM': SVC(),
            'RF': RandomForestClassifier(),
            'MLP': MLPClassifier(max_iter=5000)
        }
        scores = {
            'Model': [],
            'Train Score': [],
            'Test Score': []
        }

        for name, model in models.items():
            model.fit(self.X_train, self.y_train)
            train_score = accuracy_score(self.y_train, model.predict(self.X_train))
            test_score = accuracy_score(self.y_test, model.predict(self.X_test))
            
            scores['Model'].append(name)
            scores['Train Score'].append(train_score)
            scores['Test Score'].append(test_score)
        scores_df = pd.DataFrame(scores)
        best_model_name = scores_df.loc[scores_df['Test Score'].idxmax(), 'Model']
        best_model = models[best_model_name]
        save_model(best_model, best_model_name)
        return best_model_name

    def perform_regression_training(self, X_train, X_test, y_train, y_test):
        pass