from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class UnivariateAnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, df: pd.DataFrame, feature: str):
        pass



class NumericalUnivariateAnalysis(UnivariateAnalysisStrategy):
    def __init__(self, log_transform: bool = False):
        self.log_transform = log_transform

    def analyze(self, df: pd.DataFrame, feature: str):
        data = df[feature]
        data = data[(data > 0) & (data.notnull())]

        if data.empty:
            print(f"No valid numeric data to analyze in column: {feature}")
            return

        plt.figure(figsize=(10, 6))
        if self.log_transform:
            sns.histplot(np.log1p(data), kde=True, bins=30, color="steelblue", edgecolor="black")
            plt.title(f"Log-Transformed Distribution of '{feature}'", fontsize=14)
            plt.xlabel(f"log(1 + {feature})")
        else:
            sns.histplot(data, kde=True, bins=30, color="steelblue", edgecolor="black")
            plt.title(f"Distribution of '{feature}'", fontsize=14)
            plt.xlabel(feature)

        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()


class CategoricalUnivariateAnalysis(UnivariateAnalysisStrategy):
    def analyze(self, df: pd.DataFrame, feature: str):
        value_counts = df[feature].value_counts().head(20)
        if value_counts.empty:
            print(f"No valid categorical data to analyze in column: {feature}")
            return

        plt.figure(figsize=(12, 6))
        sns.countplot(x=feature, data=df, hue=feature, palette="muted", legend=False)
        plt.title(f"Top Categories in '{feature}'", fontsize=14)
        plt.xlabel(feature)
        plt.ylabel("Count")
        plt.xticks(rotation=45 if len(value_counts) > 5 else 0)
        plt.tight_layout()
        plt.show()


class UnivariateAnalyzer:
    def __init__(self, strategy: UnivariateAnalysisStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: UnivariateAnalysisStrategy):
        self._strategy = strategy

    def execute_analysis(self, df: pd.DataFrame, feature: str):
        self._strategy.analyze(df, feature)
