import pandas as pd
from zenml import step

@step
def dynamic_importer() -> str:
    data = {
        "Store": [1, 2, 3, 4],
        "DayOfWeek": [5, 4, 3, 2],
        "Sales": [5263, 6064, 8314, 13995],
        "Customers": [555, 625, 821, 1498],
        "Open": [1, 1, 1, 1],
        "Promo": [1, 1, 1, 1],
        "SchoolHoliday": [0, 0, 0, 0],
    }
    df = pd.DataFrame(data)
    return df.to_json(orient="split")
