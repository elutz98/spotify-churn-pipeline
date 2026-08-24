from google.cloud import bigquery

PROJECT_ID = "spotify-churn-pipeline"
DATASET_ID = "sparkify_churn"
TABLE_ID = "raw_events"
GCS_URI = "gs://spotify-churn-raw-data-elutz98/raw/mini_sparkify_event_data.json"

def load_json_to_bigquery():
    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
        write_disposition="WRITE_TRUNCATE",  # overwrite if re-run
    )

    load_job = client.load_table_from_uri(
        GCS_URI, table_ref, job_config=job_config
    )
    load_job.result()  # waits for the job to complete

    table = client.get_table(table_ref)
    print(f"Loaded {table.num_rows} rows into {table_ref}")

if __name__ == "__main__":
    load_json_to_bigquery()