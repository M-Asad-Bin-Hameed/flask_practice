from flask import Flask, render_template, request, jsonify
from src.components.logger import logger
from src.pipeline.training import TrainingPipeline
from src.pipeline.prediction import PredictionPipeline
from src.utils import get_data_details_for_prediction

app = Flask(__name__)


@app.route('/')
def home():
    logger.info('Rendering Home Page')
    return render_template('index.html')

@app.route('/training')
def training():

    logger.info('Rendering training page')
    return render_template('training.html')

@app.route('/run_training', methods=['POST'])
def train_model():
    logger.info("Model training started")
    training_pipeline = TrainingPipeline('configs/data_config.yaml')
    best_model_name = training_pipeline.train()
    logger.info("Model training ended")
    return jsonify({"status": "success","model_name": best_model_name})

@app.route('/prediction')
def prediction():
    prediction_pipeline = PredictionPipeline('configs/data_config.yaml')
    columns_info = get_data_details_for_prediction('artifacts/sample_data.csv')
    logger.info('Rendering prediction page')
    return render_template('prediction.html',
                           columns_info=columns_info)

@app.route('/run_prediction', methods=['POST'])
def run_prediction():

    logger.info('Running Prediction')
    prediction_result = '1'
    field_data = request.form.to_dict()
    logger.info('Rendering prediction result page')

    return render_template('prediction_result.html',
                            prediction_result=prediction_result)


if __name__ == '__main__':
    app.run(debug=True)
