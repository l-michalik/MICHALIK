from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class BivariateAnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, df: pd.DataFrame, feature1: str, feature2: str):
        pass


class NumericalVsNumericalAnalysis(BivariateAnalysisStrategy):
    def analyze(self, df: pd.DataFrame, feature1: str, feature2: str):
        data = df[[feature1, feature2]].dropna()

        if data.empty:
            print(f"No valid numeric data to analyze between '{feature1}' and '{feature2}'.")
            return

        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=feature1, y=feature2, data=data, alpha=0.5, edgecolor="w", linewidth=0.5)
        plt.title(f"{feature1} vs {feature2}", fontsize=14)
        plt.xlabel(feature1)
        plt.ylabel(feature2)
        plt.tight_layout()
        plt.show()


class CategoricalVsNumericalAnalysis(BivariateAnalysisStrategy):
    def analyze(self, df: pd.DataFrame, feature1: str, feature2: str):
        top_categories = df[feature1].value_counts().head(20).index
        data = df[df[feature1].isin(top_categories)][[feature1, feature2]].dropna()

        if data.empty:
            print(f"No valid data to analyze between '{feature1}' and '{feature2}'.")
            return

        plt.figure(figsize=(12, 6))
        sns.boxplot(x=feature1, y=feature2, hue=feature1, data=data, palette="Set2", legend=False)
        plt.title(f"{feature1} vs {feature2}", fontsize=14)
        plt.xlabel(feature1)
        plt.ylabel(feature2)
        plt.xticks(rotation=45 if len(top_categories) > 5 else 0)
        plt.tight_layout()
        plt.show()


class BivariateAnalyzer:
    def __init__(self, strategy: BivariateAnalysisStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: BivariateAnalysisStrategy):
        self._strategy = strategy

    def execute_analysis(self, df: pd.DataFrame, feature1: str, feature2: str):
        self._strategy.analyze(df, feature1, feature2)
