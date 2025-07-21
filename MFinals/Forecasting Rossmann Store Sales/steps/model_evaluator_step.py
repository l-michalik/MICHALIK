import logging
from typing import Tuple

import pandas as pd
from sklearn.pipeline import Pipeline
from zenml import step

from src.model_evaluator import ModelEvaluator, RegressionModelEvaluationStrategy


@step(enable_cache=False)
def model_evaluator_step(
    trained_model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series
) -> Tuple[dict, float]:
    if not isinstance(X_test, pd.DataFrame):
        raise TypeError("X_test must be a pandas DataFrame.")
    if not isinstance(y_test, pd.Series):
        raise TypeError("y_test must be a pandas Series.")

    logging.info("Evaluating model on test set.")

    y_pred = trained_model.predict(X_test)

    evaluator = ModelEvaluator(strategy=RegressionModelEvaluationStrategy())
    evaluation_metrics = evaluator.evaluate(y_pred, y_test)

    if not isinstance(evaluation_metrics, dict):
        raise ValueError("Evaluation must return a dictionary.")

    mse = evaluation_metrics.get("Mean Squared Error")
    return evaluation_metrics, mse
