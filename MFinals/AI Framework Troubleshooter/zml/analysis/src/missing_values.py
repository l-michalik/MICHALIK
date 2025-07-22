from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class MissingValuesAnalysisTemplate(ABC):
    def analyze(self, df: pd.DataFrame):
        self.identify_missing_values(df)
        self.visualize_missing_values(df)

    @abstractmethod
    def identify_missing_values(self, df: pd.DataFrame):
        pass

    @abstractmethod
    def visualize_missing_values(self, df: pd.DataFrame):
        pass


class SimpleMissingValuesAnalysis(MissingValuesAnalysisTemplate):
    def identify_missing_values(self, df: pd.DataFrame):
        print("\nMissing Values Count by Column:")
        missing_values = df.isnull().sum()
        missing_values = missing_values[missing_values > 0]

        if not missing_values.empty:
            formatted = missing_values.apply(lambda x: f"{x:,}")
            print(formatted.to_string())
        else:
            print("No missing values found in the dataset.")

    def visualize_missing_values(self, df: pd.DataFrame):
        if df.isnull().sum().sum() == 0:
            print("\nNo missing values to visualize.")
            return

        print("\nVisualizing Missing Values Heatmap...")
        plt.figure(figsize=(12, 8))
        sns.heatmap(df.isnull(), cbar=False, cmap="magma", yticklabels=False)
        plt.title("Missing Values Heatmap", fontsize=16)
        plt.xlabel("Columns")
        plt.ylabel("Rows")
        plt.tight_layout()
        plt.show()
