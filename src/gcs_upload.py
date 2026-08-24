from google.cloud import storage

# Config
PROJECT_ID = "spotify-churn-pipeline"
BUCKET_NAME = "spotify-churn-raw-data-elutz98"  # must be globally unique across ALL of GCS
LOCAL_FILE_PATH = "data/raw/mini_sparkify_event_data.json"
DESTINATION_BLOB_NAME = "raw/mini_sparkify_event_data.json"

def create_bucket(bucket_name, project_id, location="US"):
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)
    if bucket.exists():
        print(f"Bucket '{bucket_name}' already exists.")
        return bucket
    new_bucket = client.create_bucket(bucket, location=location)
    print(f"Bucket '{new_bucket.name}' created in {location}.")
    return new_bucket

def upload_file(bucket_name, source_file_path, destination_blob_name, project_id):
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    print(f"Uploaded {source_file_path} to gs://{bucket_name}/{destination_blob_name}")

if __name__ == "__main__":
    create_bucket(BUCKET_NAME, PROJECT_ID)
    upload_file(BUCKET_NAME, LOCAL_FILE_PATH, DESTINATION_BLOB_NAME, PROJECT_ID)