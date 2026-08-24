\# Spotify User Engagement \& Churn Prediction Pipeline



An end-to-end data pipeline demonstrating cloud-based ETL, SQL feature engineering,

and machine learning for churn prediction — built using Google Cloud Platform (GCS,

BigQuery), Python, and Tableau.



\## Dataset



This project uses the \*\*Sparkify mini dataset\*\* (from Udacity's Data Scientist

Nanodegree), a simulated music-streaming event log structurally similar to real

Spotify usage data. \~128MB, \~286K events, 225 unique users, sourced from

Udacity's public S3 bucket.



\## Pipeline Architecture



Raw JSON (GCS) → BigQuery (SQL feature engineering) → Python (model training) →

BigQuery (predictions write-back) → Tableau (dashboard)



\## Known Data Limitations



\- \*\*Skip rate proxy:\*\* The dataset does not include partial-play duration data,

&#x20; so a true "skip" (stopping a song early) cannot be directly measured. As a

&#x20; proxy, `average\_skip\_rate` is calculated as the ratio of "Thumbs Down" events

&#x20; to total song plays per user. This captures explicit negative feedback but

&#x20; likely understates actual skip behavior, since most skips don't come with an

&#x20; explicit thumbs-down.

\- \*\*Churn definition:\*\* A user is labeled as churned (`has\_churned = 1`) if they

&#x20; ever reach the "Cancellation Confirmation" page in the event log. This is a

&#x20; hard cutoff based on account cancellation, not a soft definition like extended

&#x20; inactivity.

\- \*\*active\_days\_in\_last\_30:\*\* Calculated relative to the last event timestamp in

&#x20; the dataset (Nov 2018), not the current date, since this is historical data.



\## Repo Structure



\- `src/` — production scripts (GCS upload, BigQuery load)

\- `sql/` — feature engineering queries

\- `notebooks/` — exploratory analysis and model development

\- `outputs/` — model metrics and evaluation results

