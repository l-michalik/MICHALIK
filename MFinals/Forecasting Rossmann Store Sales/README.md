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

python -m v2.processing.main