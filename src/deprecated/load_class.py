from google.cloud import bigquery
client = bigquery.Client()
job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("class", "STRING"),
        bigquery.SchemaField("url", "STRING"),
    ],
    skip_leading_rows=1,
    source_format=bigquery.SourceFormat.CSV,
    field_delimiter="|"
)


def load_blob(uri, table_id):
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()
    destination_table = client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))


if __name__ == "__main__":
    uri = "gs://blog-files-2024/src/posts_class.csv"
    table_id = "llm-studies.blog.posts_class"
    load_blob(uri, table_id)
