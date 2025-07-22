import pandas as pd
from src.outlier_detection import OutlierDetector, ZScoreOutlierDetection
from zenml import step


@step
def outlier_detection_step(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    if df is None:
        raise ValueError("Input df must not be None.")
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")

    df_numeric = df.select_dtypes(include=[int, float])
    detector = OutlierDetector(ZScoreOutlierDetection(threshold=3))
    return detector.handle_outliers(df_numeric, method="remove")
