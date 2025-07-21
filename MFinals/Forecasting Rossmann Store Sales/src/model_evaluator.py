import logging
from abc import ABC, abstractmethod

import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class ModelEvaluationStrategy(ABC):
    @abstractmethod
    def evaluate_model(
        self, y_pred: pd.Series, y_true: pd.Series
    ) -> dict:
        pass


class RegressionModelEvaluationStrategy(ModelEvaluationStrategy):
    def evaluate_model(
        self, y_pred: pd.Series, y_true: pd.Series
    ) -> dict:
        logging.info("Calculating regression metrics.")
        
        mse = mean_squared_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)

        metrics = {"Mean Squared Error": mse, "R-Squared": r2}

        logging.info(f"Model Evaluation Metrics: {metrics}")
        
        return metrics


class ModelEvaluator:
    def __init__(self, strategy: ModelEvaluationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ModelEvaluationStrategy):
        logging.info("Switched evaluation strategy.")
        self._strategy = strategy

    def evaluate(self, y_pred: pd.Series, y_true: pd.Series) -> dict:
        logging.info("Evaluating predictions.")
        return self._strategy.evaluate_model(y_pred, y_true)
