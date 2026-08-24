# Spotify User Engagement & Churn Prediction Pipeline

An end-to-end data pipeline demonstrating cloud-based ETL, SQL feature engineering,
and machine learning for churn prediction - built using Google Cloud Platform (GCS,
BigQuery), Python, and Tableau.

## Dataset

This project uses the **Sparkify mini dataset** (from Udacity's Data Scientist
Nanodegree), a simulated music-streaming event log structurally similar to real
Spotify usage data. ~128MB, ~286K events, 225 unique users, sourced from
Udacity's public S3 bucket.

## Pipeline Architecture

Raw JSON (GCS) -> BigQuery (SQL feature engineering) -> Python (model training) ->
BigQuery (predictions write-back) -> Tableau (dashboard)

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

- src/ - production scripts (GCS upload, BigQuery load)
- sql/ - feature engineering queries
- notebooks/ - exploratory analysis and model development
- outputs/ - model metrics and evaluation results
