import click
from pipelines.training_pipeline import ml_pipeline
from zenml.integrations.mlflow.mlflow_utils import get_tracking_uri

@click.command()
def main():
    ml_pipeline()

    tracking_uri = get_tracking_uri()
    print(
        "\n✅ Pipeline executed successfully!"
        "\nTo inspect your experiment runs, launch the MLflow UI with:"
        f"\n\n    mlflow ui --backend-store-uri '{tracking_uri}'\n"
    )


if __name__ == "__main__":
    main()
