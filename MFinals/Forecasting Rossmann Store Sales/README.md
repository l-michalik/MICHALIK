## Target
You are provided with historical sales data for 1,115 Rossmann stores. The task is to forecast the "Sales" column for the test set. Note that some stores in the dataset were temporarily closed for refurbishment.

## Source
@misc{rossmann-store-sales,
    author = {FlorianKnauer and Will Cukierski},
    title = {Rossmann Store Sales},
    year = {2015},
    howpublished = {\url{https://kaggle.com/competitions/rossmann-store-sales}},
    note = {Kaggle}
}

i opt to enirich data with 3 additional sources: weather, store states and store states google trend

python -m v3.extracting.main

v2/
├── main.py                           # Główne wejście do pipeline'u
├── config/                           # Konfiguracja / parametry
│   └── settings.py
├── data/                             # Ścieżki do danych wejściowych/wyjściowych (puste, .gitkeep)
│   ├── raw/
│   ├── processed/
│   └── interim/
├── extracting/                       # Moduły ekstrakcji danych
│   ├── __init__.py
│   ├── base.py                       # Klasa bazowa dla ekstraktorów
│   ├── weather.py                    # Dane pogodowe
│   ├── google.py                     # Dane z Google
│   └── backward.py                   # Ekstrakcja cech czasowych wstecz
├── preparing/                        # Przygotowanie danych do modelowania
│   ├── __init__.py
│   ├── prepare_dataset.py
│   └── features_nn.py                # Przygotowanie cech dla sieci
├── models/                           # Modele ML/NN
│   ├── __init__.py
│   ├── base_model.py                 # Klasa bazowa
│   ├── nn_entity_embedding.py        # Twój model NN_with_EntityEmbedding
│   └── train.py                      # Trening i ewaluacja modeli
├── utils/                            # Pomocnicze narzędzia
│   ├── __init__.py
│   ├── constants.py
│   └── io.py                         # np. zapisywanie modeli/predykcji
├── notebooks/                        # Notebooki eksploracyjne (jeśli używasz)
└── README.md

przepisz go wysokiej klasy kod jakby pisal go senior python developer i nie rob tego na slepo tylko sie zastanow czy ten kod nie jest przestarzaly i np. formy zapisu pickle sa dobre - zrob to najlepiej jak sie da i ma to byc na miare 2025 roku, jesli cos nadaje sie do wydzielenia do utils to zaznacz to