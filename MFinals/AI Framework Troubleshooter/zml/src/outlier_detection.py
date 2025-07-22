import logging
from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class OutlierDetectionStrategy(ABC):
    @abstractmethod
    def detect_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        pass


class ZScoreOutlierDetection(OutlierDetectionStrategy):
    def __init__(self, threshold=3):
        self.threshold = threshold

    def detect_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        z_scores = np.abs((df - df.mean()) / df.std())
        return z_scores > self.threshold


class IQROutlierDetection(OutlierDetectionStrategy):
    def detect_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        Q1 = df.quantile(0.25)
        Q3 = df.quantile(0.75)
        IQR = Q3 - Q1
        return (df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))


class OutlierDetector:
    def __init__(self, strategy: OutlierDetectionStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: OutlierDetectionStrategy):
        self._strategy = strategy

    def detect_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        return self._strategy.detect_outliers(df)

    def handle_outliers(self, df: pd.DataFrame, method="remove", **kwargs) -> pd.DataFrame:
        outliers = self.detect_outliers(df)
        if method == "remove":
            return df[(~outliers).all(axis=1)]
        elif method == "cap":
            return df.clip(lower=df.quantile(0.01), upper=df.quantile(0.99), axis=1)
        return df

    def visualize_outliers(self, df: pd.DataFrame, features: list):
        for feature in features:
            plt.figure(figsize=(10, 6))
            sns.boxplot(x=df[feature])
            plt.title(f"Boxplot of {feature}")
            plt.show()


if __name__ == "__main__":
    pass
