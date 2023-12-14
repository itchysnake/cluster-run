from google.cloud import storage

def upload(bucket, filename, data):
    gcs = storage.Client()
    bucket = gcs.get_bucket(bucket)
    blob = bucket.blob(filename)

    blob.upload_from_string(
        data=data,
        content_type="text/csv"
    )

    return "OK"