import pickle
import math
import os
from datetime import datetime
from isoweek import Week

def abc2int(char: str) -> int:
    return {'0': 0, 'a': 1, 'b': 2, 'c': 3, 'd': 4}.get(char, 0)

def state2int(state: str) -> int:
    return {
        'HB,NI': 0, 'HH': 1, 'TH': 2, 'RP': 3, 'ST': 4,
        'BW': 5, 'SN': 6, 'BE': 7, 'HE': 8, 'SH': 9, 'BY': 10, 'NW': 11
    }.get(state, -1)

def PromoInterval2int(interval: str) -> int:
    return {'0': 0, 'J': 1, 'F': 2, 'M': 3}.get(interval[0] if interval else '0', 0)

def has_competition_months(date, year, month):
    if year == 0:
        return 0
    open_date = datetime(year=year, month=month, day=15)
    delta_months = (date - open_date).days // 30
    return max(0, min(delta_months, 24))

def has_promo2_weeks(date, year, week):
    if year == 0:
        return 0
    start_date = Week(year, week).monday()
    delta_weeks = (date.date() - start_date).days // 7
    return max(0, min(delta_weeks, 25))

def latest_promo2_months(date, interval, year, week):
    if not has_promo2_weeks(date, year, week):
        return 0
    month_code = PromoInterval2int(interval)
    if month_code == 0:
        return 0
    if date.month < month_code:
        promo_year = date.year - 1
        promo_month = month_code + 9
    else:
        promo_year = date.year
        promo_month = ((date.month - month_code) // 3) * 3 + month_code
    promo_start = datetime(promo_year, promo_month, 1)
    return (date - promo_start).days // 30

def safe_int(val, default=0):
    try:
        return int(val)
    except (ValueError, TypeError):
        return default

def load_pickle_data():
    with open('./pickles/train_data.pickle', 'rb') as f:
        train_data = pickle.load(f)
    with open('./pickles/test_data.pickle', 'rb') as f:
        test_data = pickle.load(f)
    with open('./pickles/store_data.pickle', 'rb') as f:
        store_data = pickle.load(f)
    with open('./pickles/weather.pickle', 'rb') as f:
        weather = pickle.load(f)
    with open('./pickles/fb.pickle', 'rb') as f:
        fb = pickle.load(f)
    with open('./pickles/google_trends.pickle', 'rb') as f:
        trends = pickle.load(f)

    return train_data, test_data, store_data, weather, fb, trends


def extract_features(record, store_data, weather, fb, trends):
    dt = datetime.strptime(record['Date'], '%Y-%m-%d')
    store_idx = safe_int(record['Store']) - 1
    store = store_data[store_idx]

    features = [
        safe_int(record.get('Open', 1)),
        safe_int(record['Store']),
        safe_int(record['DayOfWeek']),
        safe_int(record['Promo']),
        dt.year,
        dt.month,
        dt.day,
        abc2int(record.get('StateHoliday', '0')),
        safe_int(record.get('SchoolHoliday')),
        has_competition_months(dt, safe_int(store.get('CompetitionOpenSinceYear')), safe_int(store.get('CompetitionOpenSinceMonth'))),
        has_promo2_weeks(dt, safe_int(store.get('Promo2SinceYear')), safe_int(store.get('Promo2SinceWeek'))),
        latest_promo2_months(dt, store.get('PromoInterval', ''), safe_int(store.get('Promo2SinceYear')), safe_int(store.get('Promo2SinceWeek'))),
        math.log1p(safe_int(store.get('CompetitionDistance'))) / 10,
        abc2int(store.get('StoreType', '0')),
        abc2int(store.get('Assortment', '0')),
        PromoInterval2int(store.get('PromoInterval', '0')),
        safe_int(store.get('CompetitionOpenSinceYear')),
        safe_int(store.get('Promo2SinceYear')),
        state2int(store.get('State')),
        dt.isocalendar()[1]
    ]

    weather_key = (store['State'], record['Date'])
    fb_key = (int(record['Store']), record['Date'])
    trend_keys = [
        ('DE', dt.year, dt.isocalendar()[1]),
        (store['State'], dt.year, dt.isocalendar()[1])
    ]

    features.extend(weather.get(weather_key, [0.0] * 9))
    features.extend([int(v) for v in fb.get(fb_key, [0] * 8)])
    features.extend([trends.get(k, 0.0) for k in trend_keys])

    return features


def generate_dataset():
    train_data, test_data, store_data, weather, fb, trends = load_pickle_data()

    X_train, y_train = [], []
    for r in train_data:
        if r['Sales'] != '0' and r.get('Open', '1') != '':
            X_train.append(extract_features(r, store_data, weather, fb, trends))
            y_train.append(int(r['Sales']))

    print(f"Train samples: {len(y_train)} | Sales range: {min(y_train)} - {max(y_train)}")

    X_test = [extract_features(r, store_data, weather, fb, trends) for r in test_data]
    print(f"Test samples: {len(X_test)}")

    os.makedirs('pickles', exist_ok=True)
    with open('pickles/feature_train_data.pickle', 'wb') as f:
        pickle.dump((X_train, y_train), f, protocol=pickle.HIGHEST_PROTOCOL)
    with open('pickles/feature_test_data.pickle', 'wb') as f:
        pickle.dump(X_test, f, protocol=pickle.HIGHEST_PROTOCOL)

    print("Feature engineering complete. Pickles saved in ./pickles/.")

if __name__ == "__main__":
    generate_dataset()
