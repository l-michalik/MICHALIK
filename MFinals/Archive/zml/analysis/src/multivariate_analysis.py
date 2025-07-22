from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class MultivariateAnalysisTemplate(ABC):
    def analyze(self, df: pd.DataFrame):
        self.generate_correlation_heatmap(df)
        self.generate_pairplot(df)

    @abstractmethod
    def generate_correlation_heatmap(self, df: pd.DataFrame):
        pass

    @abstractmethod
    def generate_pairplot(self, df: pd.DataFrame):
        pass


class SimpleMultivariateAnalysis(MultivariateAnalysisTemplate):
    def generate_correlation_heatmap(self, df: pd.DataFrame):
        numeric_df = df.select_dtypes(include='number').dropna()
        corr = numeric_df.corr()

        plt.figure(figsize=(12, 10))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, square=True, cbar_kws={'shrink': .5})
        plt.title("Correlation Heatmap", fontsize=16)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()

    def generate_pairplot(self, df: pd.DataFrame):
        numeric_df = df.select_dtypes(include='number').dropna()

        # Limit to 6 features max for pairplot to avoid overcrowding
        top_features = numeric_df.corr().abs().sum().sort_values(ascending=False).head(6).index.tolist()
        limited_df = numeric_df[top_features]

        sns.pairplot(limited_df, diag_kind="kde")
        plt.suptitle("Pair Plot of Top Correlated Features", y=1.02)
        plt.show()
