## Target
You are provided with historical sales data for 1,115 Rossmann stores. The task is to forecast the "Sales" column for the test set. Note that some stores in the dataset were temporarily closed for refurbishment.

## Install ZenML
👉 https://docs.zenml.io/getting-started/installation

zenml integration install mlflow -y
zenml experiment-tracker register mlflow_tracker --flavor=mlflow
zenml model-deployer register mlflow --flavor=mlflow
zenml stack register local-mlflow-stack -a default -o default -d mlflow -e mlflow_tracker --set

## Source
@misc{rossmann-store-sales,
    author = {FlorianKnauer and Will Cukierski},
    title = {Rossmann Store Sales},
    year = {2015},
    howpublished = {\url{https://kaggle.com/competitions/rossmann-store-sales}},
    note = {Kaggle}
}

i opt to enirich data with 3 additional sources: weather, store states and store states google trend

python -m extracting.main

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


\\
- czemu taka libka a nie inna
\\

---
- first undarstand the data then do eda

- ```export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES 
zenml up```

-

---
mlflow ui --backend-store-uri 'file:/Users/lukaszmichalik/Library/Application Support/zenml/local_stores/917fd007-db63-4a6b-95fe-8f25c59fd3ad/mlruns'