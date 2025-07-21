import logging
from typing import Annotated

import mlflow
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from zenml import step, ArtifactConfig, Model
from zenml.client import Client

experiment_tracker = Client().active_stack.experiment_tracker

model = Model(
    name="prices_predictor",
    license="Apache 2.0",
    description="Price prediction model for houses.",
)

@step(enable_cache=False, experiment_tracker=experiment_tracker.name, model=model)
def model_building_step(
    X_train: pd.DataFrame, y_train: pd.Series
) -> Annotated[Pipeline, ArtifactConfig(name="sklearn_pipeline", is_model_artifact=True)]:
    categorical = X_train.select_dtypes(include=["object", "category"]).columns
    numerical = X_train.select_dtypes(exclude=["object", "category"]).columns

    logging.info(f"Categorical: {categorical.tolist()}")
    logging.info(f"Numerical: {numerical.tolist()}")

    preprocessor = ColumnTransformer([
        ("num", SimpleImputer(strategy="mean"), numerical),
        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]), categorical)
    ])

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", LinearRegression())
    ])

    mlflow.sklearn.autolog()
    with mlflow.start_run():
        pipeline.fit(X_train, y_train)

        encoder = pipeline.named_steps["preprocessor"].transformers_[1][1].named_steps["onehot"]
        encoder.fit(X_train[categorical])
        expected_columns = numerical.tolist() + list(encoder.get_feature_names_out(categorical))
        logging.info(f"Expected model columns: {expected_columns}")

    return pipeline
