# Forecasting Rossmann Store Sales

## Project Overview

This project focuses on predicting daily sales for 1,115 Rossmann stores located across Germany. The historical data includes information on promotions, holidays, and store-specific features. To enhance the model’s accuracy and generalization, the data is enriched with several external sources that reflect real-world conditions influencing customer behavior.

---

## Data Source

The core dataset comes from the Kaggle competition:  
https://www.kaggle.com/competitions/rossmann-store-sales

---

## Why External Data?

Store managers across 1,100+ locations are expected to forecast daily sales up to 6 weeks ahead. But relying only on internal store-level data is limiting. Local factors such as weather, search interest, and regional characteristics significantly impact foot traffic and purchasing patterns.

To address this, I enriched the dataset with:

- **Weather data**
- **Google Trends**
- **Store states**

These features help the model better understand context and variation between different regions and time periods.

---

## forwardback.py: Time-Aware Feature Engineering

One key component of the pipeline is the generation of **forward and backward-looking features**. These capture temporal distances to and from special events such as promotions and holidays.

For each date and store, we compute:

- Days since / until the next:
  - `Promo`
  - `SchoolHoliday`
  - `StateHoliday`
- Event counts in a past/future time window (for holidays)

This is implemented using an efficient timestamp accessor, avoiding full re-scans of the time array. The logic is particularly useful for modeling customer anticipation or delayed effects (e.g., increased shopping before holidays).

---

## Project Structure

```
.
├── extracting/        # External data: weather, Google Trends, forward-back features
├── preparing/         # Dataset preparation and feature merging
├── models/            # Model training and evaluation
├── utils/             # Helper functions (e.g., file I/O)
├── view/              # Jupyter notebooks for EDA
├── model.py           # End-to-end runner
├── requirements.txt   # Dependencies
└── README.md
```

---

## How to Run

```bash
   python model.py
```

---

## Summary

By combining internal records with external data (weather, trends, store context), this project builds a more reliable and regionally aware forecast engine. The goal is not just accuracy, but also practicality — empowering Rossmann stores to make better staffing and stock decisions based on smarter predictions.