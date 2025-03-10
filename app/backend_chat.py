from google.cloud import bigquery
from bq_chat_queries import BQ_chat_queries

def qa(prompt):
    client = bigquery.Client()
    bq_chat_queries = BQ_chat_queries(prompt) 
    query = bq_chat_queries.query_qa
    print(f"QUERY {query}")
    rows = client.query_and_wait(query)
    print(f"rows to be checked... {rows.total_rows}")
    for row in rows:
        print("post={}".format(row["post_title"]))
        return row["post_title"]

def rag(prompt):
    client = bigquery.Client()
    bq_chat_queries = BQ_chat_queries(prompt) 
    query = bq_chat_queries.query_rag
    print(f"QUERY {query}")
    rows = client.query_and_wait(query)
    print(f"rows to be checked... {rows.total_rows}")
    for row in rows:
        print("post={}".format(row["generated"]))
        return row["generated"]
