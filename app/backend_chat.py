import os
from dotenv import load_dotenv
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_community import BigQueryVectorStore
from langchain import hub
from langchain.chat_models import init_chat_model
from google.cloud import bigquery
from bq_chat_queries import BQ_chat_queries
from langchain import hub

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

def rag2(question):    
    load_dotenv()
    PROJECT_ID = os.getenv("PROJECT_ID") 
    LOCATION = os.getenv("EMB_LOCATION") 
    DATASET = os.getenv("DATASET") 
    TABLE = os.getenv("TABLE") 
    embeddings = VertexAIEmbeddings(model="textembedding-gecko@latest")
    vector_store = BigQueryVectorStore(
        project_id=PROJECT_ID,
        dataset_name=DATASET,
        table_name=TABLE,
        location=LOCATION,
        embedding=embeddings,
    )
    retrieved_docs = vector_store.similarity_search(
        question,
        k=2,
#        filter={"doc_id": "4169c3a6102540149ae4d0de6cbf06f2"},
    )
    prompt = hub.pull("rlm/rag-prompt")
    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
    prompt = prompt.invoke({"question": question, "context": docs_content})
    llm = init_chat_model("gemini-2.0-flash-001", model_provider="google_vertexai")
    answer = llm.invoke(prompt)
    return answer.content