import json
import numpy as np
import pandas as pd
from zenml import step
from zenml.integrations.mlflow.services import MLFlowDeploymentService

@step(enable_cache=False)
def predictor(
    service: MLFlowDeploymentService,
    input_data: str,
) -> np.ndarray:
    service.start(timeout=10)
    data = json.loads(input_data)
    data.pop("columns", None)
    data.pop("index", None)

    expected_columns = [
        "Store",
        "DayOfWeek",
        "Sales",
        "Customers",
        "Open",
        "Promo",
        "SchoolHoliday",
    ]

    df = pd.DataFrame(data["data"], columns=expected_columns)
    json_list = json.loads(json.dumps(list(df.T.to_dict().values())))
    data_array = np.array(json_list)
    prediction = service.predict(data_array)
    return prediction
