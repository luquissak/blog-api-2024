from google.cloud import bigquery
client = bigquery.Client()
table_id = "llm-studies.blog.posts_dez_2024"
schema = [
    bigquery.SchemaField("blog_id", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("post_id", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("log_date", "DATETIME", mode="REQUIRED"),
    bigquery.SchemaField("post_date", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("post_wday", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("post_url", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("post_title", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("post_content_html", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("post_content", "STRING", mode="REQUIRED"),
    #bigquery.SchemaField("post_replies", "STRING", mode="REPEATED"),
    bigquery.SchemaField(
        "post_labels",
        "STRING",
        mode="REPEATED"),

]

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)
print(
    "Created table {}.{}.{}".format(
        table.project, table.dataset_id, table.table_id)
)
