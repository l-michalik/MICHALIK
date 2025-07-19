from abc import ABC, abstractmethod
import pandas as pd
from IPython.display import display

class DataInspectionStrategy(ABC):
    @abstractmethod
    def inspect(self, df: pd.DataFrame) -> None:
        pass

class DataTypesInspectionStrategy(DataInspectionStrategy):
    def inspect(self, df: pd.DataFrame) -> None:
        print("\nData Types and Non-null Counts:")
        df.info()

class SummaryStatisticsInspectionStrategy(DataInspectionStrategy):
    def inspect(self, df: pd.DataFrame) -> None:
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", 1000)

        print("\nSummary Statistics (Numerical Features):")
        numeric_summary = df.describe().copy()

        formatted_summary = numeric_summary.applymap(lambda x: "{:,.0f}".format(x) if pd.notnull(x) else "")

        print(formatted_summary.to_string())

        print("\nSummary Statistics (Categorical Features):")
        display(df.describe(include=["O"]))


class DataInspector:
    def __init__(self, strategy: DataInspectionStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: DataInspectionStrategy) -> None:
        self._strategy = strategy

    def execute_inspection(self, df: pd.DataFrame) -> None:
        self._strategy.inspect(df)

if __name__ == "__main__":
    pass
