from google.cloud import storage


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    generation_match_precondition = 0
    blob.upload_from_filename(
        source_file_name, if_generation_match=generation_match_precondition)
    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


if __name__ == "__main__":
    bucket_name = "blog-files-2024"
    source_file_name = "files\posts_class.csv"
    destination_blob_name = "src/posts_class.csv"
    upload_blob(bucket_name, source_file_name, destination_blob_name)