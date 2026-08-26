"""
Exports churn predictions from BigQuery to a local CSV for Tableau Public
to connect to. Re-run any time the model is retrained to refresh the
Tableau data source.
"""

from google.cloud import bigquery

PROJECT_ID = "spotify-churn-pipeline"
SOURCE_TABLE = "spotify-churn-pipeline.sparkify_churn.churn_predictions"
OUTPUT_PATH = "outputs/churn_predictions_for_tableau.csv"


def export_predictions():
    client = bigquery.Client(project=PROJECT_ID)

    query = f"SELECT * FROM `{SOURCE_TABLE}`"
    df = client.query(query).to_dataframe()

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Exported {len(df)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    export_predictions()