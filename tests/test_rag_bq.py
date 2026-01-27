
PROJECT_ID = "llm-studies"
LOCATION = "us-central1"
DATASET = "blog2"
TABLE = "blog_emb"

from langchain_google_vertexai import VertexAIEmbeddings

embedding = VertexAIEmbeddings(
    model_name="textembedding-gecko@latest", project=PROJECT_ID
)

from langchain_google_community import BigQueryVectorStore

store = BigQueryVectorStore(
    project_id=PROJECT_ID,
    dataset_name=DATASET,
    table_name=TABLE,
    location=LOCATION,
    embedding=embedding,
)

all_texts = ["Apples and oranges", "Cars and airplanes", "Pineapple", "Train", "Banana"]
metadatas = [{"len": len(t)} for t in all_texts]

store.add_texts(all_texts, metadatas=metadatas)

query = "I'd like a fruit."
docs = store.similarity_search(query)
print(docs)

