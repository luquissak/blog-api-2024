from google.cloud import bigquery
client = bigquery.Client()
table_id = "llm-studies.blog.posts_authors"
schema = [
    bigquery.SchemaField(
        "authors",
        "STRING",
        mode="REPEATED"),
    bigquery.SchemaField("theme", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("area", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("url", "STRING", mode="REQUIRED"),
]

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)
print(
    "Created table {}.{}.{}".format(
        table.project, table.dataset_id, table.table_id)
)
