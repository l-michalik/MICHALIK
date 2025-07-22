import logging
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Dict
import math
from joblib import load, dump

from v3.utils.main import (
    safe_int, abc2int, state2int, promo_interval2int,
    has_competition_months, has_promo2_weeks, latest_promo2_months, save_joblib
)

logger = logging.getLogger(__name__)
from v3.config import Config

JOBLIB_DIR = Config.JOBLIB_DIR

def load_joblib_data() -> Tuple[list, list, list, dict, dict, dict]:
    def _load(path: Path):
        if not path.exists():
            raise FileNotFoundError(f"Missing file: {path}")
        return load(path)

    return (
        _load(JOBLIB_DIR / "train_data.joblib"),
        _load(JOBLIB_DIR / "test_data.joblib"),
        _load(JOBLIB_DIR / "store_data.joblib"),
        _load(JOBLIB_DIR / "weather.joblib"),
        _load(JOBLIB_DIR / "forwardback.joblib"),
        _load(JOBLIB_DIR / "google.joblib"),
    )

from datetime import datetime
from typing import List, Dict, Tuple
import math

def extract_features(
    record: dict,
    store_data: List[dict],
    weather: Dict[Tuple[str, str], List[float]],
    fb: Dict[Tuple[int, str], List[int]],
    trends: Dict[Tuple[str, int, int], float]
) -> List[float]:
    try:
        dt = datetime.strptime(record['Date'], '%Y-%m-%d')
        store_id = safe_int(record['Store'])

        store_map = {safe_int(s['Store']): s for s in store_data}

        if store_id not in store_map:
            raise ValueError(f"Store ID {store_id} not found in store_data.")

        store = store_map[store_id]

        features = [
            safe_int(record.get('Open', 1)),
            store_id,
            safe_int(record['DayOfWeek']),
            safe_int(record['Promo']),
            dt.year, dt.month, dt.day,
            abc2int(record.get('StateHoliday', '0')),
            safe_int(record.get('SchoolHoliday')),
            has_competition_months(dt, safe_int(store.get('CompetitionOpenSinceYear')), safe_int(store.get('CompetitionOpenSinceMonth'))),
            has_promo2_weeks(dt, safe_int(store.get('Promo2SinceYear')), safe_int(store.get('Promo2SinceWeek'))),
            latest_promo2_months(dt, store.get('PromoInterval', ''), safe_int(store.get('Promo2SinceYear')), safe_int(store.get('Promo2SinceWeek'))),
            math.log1p(safe_int(store.get('CompetitionDistance'))) / 10,
            abc2int(store.get('StoreType', '0')),
            abc2int(store.get('Assortment', '0')),
            promo_interval2int(store.get('PromoInterval', '0')),
            safe_int(store.get('CompetitionOpenSinceYear')),
            safe_int(store.get('Promo2SinceYear')),
            state2int(store.get('State')),
            dt.isocalendar()[1],
        ]

        weather_key = (store['State'], record['Date'])
        fb_key = (store_id, record['Date'])
        trend_keys = [
            ('DE', dt.year, dt.isocalendar()[1]),
            (store['State'], dt.year, dt.isocalendar()[1])
        ]

        features.extend(weather.get(weather_key, [0.0] * 9))
        features.extend([int(v) for v in fb.get(fb_key, [0] * 8)])
        features.extend([trends.get(k, 0.0) for k in trend_keys])

        return features

    except Exception as e:
        print(f"Error processing record: {record}")
        print(f"Exception: {e}")
        return []


def prepare_dataset() -> None:
    logger.info("Loading joblib data...")
    train_data, test_data, store_data, weather, fb, trends = load_joblib_data()

    X_train, y_train = [], []
    for r in train_data:
        if r['Sales'] != '0' and r.get('Open', '1') != '':
            X_train.append(extract_features(r, store_data, weather, fb, trends))
            y_train.append(int(r['Sales']))

    logger.info(f"Train samples: {len(y_train)} | Sales range: {min(y_train)} - {max(y_train)}")

    X_test = [extract_features(r, store_data, weather, fb, trends) for r in test_data]
    logger.info(f"Test samples: {len(X_test)}")

    JOBLIB_DIR.mkdir(parents=True, exist_ok=True)
    save_joblib((X_train, y_train), JOBLIB_DIR / "feature_train_data.joblib")
    save_joblib(X_test, JOBLIB_DIR / "feature_test_data.joblib")

    logger.info("Feature engineering complete. Files saved in ./artifacts/.")

if __name__ == "__main__":
    prepare_dataset()
