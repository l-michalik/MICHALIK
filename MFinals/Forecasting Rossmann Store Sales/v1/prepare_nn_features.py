import numpy as np


def CompetitionOpenSinceYear2int(since_year_array):
    # Zamienia rok otwarcia konkurencji na liczbę całkowitą (normalizowaną)
    since_year_array = since_year_array.copy()
    return np.where(since_year_array < 2000, 1, since_year_array - 1998)


def Promo2SinceYear2int(year_array):
    # Przesuwa lata Promo2 względem 2008 roku
    year_array = year_array.copy()
    shifted = year_array - 2008
    return np.where(shifted < 0, 0, shifted)


def split_features(X):
    X = np.array(X)
    X_list = []

    # Id sklepu (0-indeksowane)
    X_list.append(X[..., [1]] - 1)

    # Dzień tygodnia (0-indeksowane)
    X_list.append(X[..., [2]] - 1)

    # Promocja (binary)
    X_list.append(X[..., [3]])

    # Rok (2013 = 0)
    X_list.append(X[..., [4]] - 2013)

    # Miesiąc (0-indeksowane)
    X_list.append(X[..., [5]] - 1)

    # Dzień miesiąca (0-indeksowane)
    X_list.append(X[..., [6]] - 1)

    # Święto państwowe (kategoria numeryczna)
    X_list.append(X[..., [7]])

    # Ferie szkolne (binary)
    X_list.append(X[..., [8]])

    # Liczba miesięcy obecności konkurencji
    X_list.append(X[..., [9]])

    # Liczba tygodni obecności Promo2
    X_list.append(X[..., [10]])

    # Miesiące od ostatniego Promo2
    X_list.append(X[..., [11]])

    # Logarytm dystansu (przeskalowany)
    X_list.append(X[..., [12]])

    # Typ sklepu (zakodowany numerycznie)
    X_list.append(X[..., [13]])

    # Asortyment (zakodowany numerycznie)
    X_list.append(X[..., [14]])

    # Interwał promocji (zakodowany numerycznie)
    X_list.append(X[..., [15]])

    # Rok konkurencji (przekształcony)
    X_list.append(CompetitionOpenSinceYear2int(X[..., [16]]))

    # Rok Promo2 (przekształcony)
    X_list.append(Promo2SinceYear2int(X[..., [17]]))

    # Stan (kategoria numeryczna)
    X_list.append(X[..., [18]])

    # Tydzień roku (0-indeksowane)
    X_list.append(X[..., [19]] - 1)

    # Pogoda: temperatura (3 kolumny)
    X_list.append(X[..., [20, 21, 22]])

    # Pogoda: wilgotność (3 kolumny)
    X_list.append(X[..., [23, 24, 25]])

    # Pogoda: wiatr (2 kolumny)
    X_list.append(X[..., [26, 27]])

    # Zachmurzenie (1 kolumna)
    X_list.append(X[..., [28]])

    # Zdarzenia pogodowe (kategoryczne)
    X_list.append(X[..., [29]])

    # FB features - promo
    X_list.append(X[..., [30]] - 1)  # forward
    X_list.append(X[..., [31]] - 1)  # backward

    # FB features - state holiday
    X_list.append(X[..., [32]] - 1)
    X_list.append(X[..., [33]] - 1)
    X_list.append(X[..., [34]])
    X_list.append(X[..., [35]])

    # FB features - school holiday
    X_list.append(X[..., [36]] - 1)
    X_list.append(X[..., [37]] - 1)

    # Google trends (DE, stan)
    X_list.append(X[..., [38]])
    X_list.append(X[..., [39]])

    return X_list
