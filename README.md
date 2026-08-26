# Spotify User Engagement & Churn Prediction Pipeline

An end-to-end data pipeline demonstrating cloud-based ETL, SQL feature engineering,
and machine learning for churn prediction - built using Google Cloud Platform (GCS,
BigQuery), Python, and Google Looker Studio.

## Live Dashboard

[View the interactive Looker Studio dashboard](https://datastudio.google.com/reporting/d43c10fa-0d8f-41e9-acde-a6b6bc38f630)

## Dataset

This project uses the **Sparkify mini dataset** (from Udacity's Data Scientist
Nanodegree), a simulated music-streaming event log structurally similar to real
Spotify usage data. ~128MB, ~286K events, 225 unique users, sourced from
Udacity's public S3 bucket.

## Pipeline Architecture

Raw JSON (GCS) -> BigQuery (SQL feature engineering) -> Python (model training) ->
BigQuery (predictions write-back) -> Looker Studio (dashboard)

Note: The original design targeted Tableau Public for the BI layer. Tableau
Public's free edition does not support a live BigQuery connection (that
connector is limited to paid Tableau Desktop/Server/Cloud), so Looker Studio
was used instead, connecting live and natively to BigQuery.

## Model

A Random Forest classifier was trained on four engagement features
(total_listening_hours, average_skip_rate, active_days_in_last_30, total_events)
to predict churn.

- ROC-AUC: 0.911
- Precision (churn class): 0.78
- Recall (churn class): 0.70
- Classification threshold: 0.35, tuned to favor recall over precision, since
  in a retention context missing an at-risk user is more costly than a
  low-cost false-positive outreach

Feature importance showed active_days_in_last_30 as the dominant predictor
(51% importance), consistent with recency-of-engagement being a strong churn
signal in subscription businesses generally.

## Known Data Limitations

- **Skip rate proxy:** The dataset does not include partial-play duration data,
  so a true "skip" (stopping a song early) cannot be directly measured. As a
  proxy, average_skip_rate is calculated as the ratio of "Thumbs Down" events
  to total song plays per user. This captures explicit negative feedback but
  likely understates actual skip behavior, since most skips don't come with an
  explicit thumbs-down.
- **Churn definition:** A user is labeled as churned (has_churned = 1) if they
  ever reach the "Cancellation Confirmation" page in the event log. This is a
  hard cutoff based on account cancellation, not a soft definition like extended
  inactivity.
- **active_days_in_last_30:** Calculated relative to the last event timestamp in
  the dataset (Nov 2018), not the current date, since this is historical data.

## Repo Structure

- src/ - production scripts (GCS upload, BigQuery load, model training/prediction, Tableau/BI export)
- sql/ - feature engineering queries
- notebooks/ - exploratory analysis and model development
- outputs/ - model metrics and evaluation results
