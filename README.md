




salvar no smith as chamadas
logar as conversas










# Introduction

Python project to explore and analyze the reflections hosted in the blog https://www.reflexoesdofilosofo.blog.br/

# Getting Started

1. Requirements: Python, VSCode
2. Clone repo:

```bash
git clone git@github.com:luquissak/blog-api-2024.git
```

3. Create venv

```bash
py -m venv .venv
.venv\scripts\activate
#pip freeze >  requirements.txt
pip install -r requirements.txt
python -m ensurepip
```

4. Google Setup

```bash
gcloud auth login
gcloud components update
gcloud auth application-default login
gcloud config set project llm-studies
gcloud auth application-default set-quota-project llm-studies
gcloud config list
```

# Build and Test

```bash
$env:GOOGLE_APPLICATION_CREDENTIALS="credentials\client_secret_129125337363-uci7et766rno47m5p4m2tfukr8b3d1dd.apps.googleusercontent.com.json"
.venv\scripts\activate && .venv\Scripts\python.exe src\post_list.py
.venv\scripts\activate && .venv\Scripts\python.exe src\get_posts.py
.venv\scripts\activate && .venv\Scripts\python.exe test\post_date_format.py
.venv\scripts\activate && .venv\Scripts\python.exe test\docx_to_pdf.py
.venv\scripts\activate && .venv\Scripts\python.exe src\get_posts_files.py
.venv\scripts\activate && .venv\Scripts\python.exe src\convert_to_pdf.py
.venv\scripts\activate && .venv\Scripts\python.exe test\post_fields.py
.venv\scripts\activate && .venv\Scripts\python.exe src\get_comments.py
#--noauth_local_webserver
```

# BQ Analysis

Create connection

```bash
bq mk --connection --location=us --project_id=llm-studies --connection_type=CLOUD_RESOURCE to-vertex-us-g
bq show --connection llm-studies.us.to-vertex-us-g
gcloud projects add-iam-policy-binding 129125337363 --member='serviceAccount:bqcx-129125337363-4se3@gcp-sa-bigquery-condel.iam.gserviceaccount.com' --role='roles/aiplatform.user' --condition=None
```

Create model: text-embedding-004

```bash
CREATE OR REPLACE MODEL `llm-studies.blog.text_emb`
REMOTE WITH CONNECTION `129125337363.us.to-vertex-us-g`
OPTIONS (ENDPOINT = 'text-embedding-004');
```


Create model: gemini-1.5-flash-002

```bash
CREATE OR REPLACE MODEL `llm-studies.blog.text_model`
  REMOTE WITH CONNECTION `129125337363.us.to-vertex-us-g`
  OPTIONS (ENDPOINT = 'gemini-1.5-flash-002');
```

Create embeddings

```bash
CREATE OR REPLACE TABLE `llm-studies.blog.posts_dez_2024_emb`
as
SELECT * FROM ML.GENERATE_TEXT_EMBEDDING(
   MODEL `llm-studies.blog.text_emb`,
   (SELECT *, post_content as content FROM `llm-studies.blog.posts_dez_2024`)
)
```

Create index: ERR (Total rows 435 is smaller than min allowed 5000 for CREATE VECTOR INDEX query with the IVF index type. Please use VECTOR_SEARCH table-valued function directly to perform the similarity search.)

```bash
CREATE OR REPLACE VECTOR INDEX `llm-studies.blog.post_content_index`
ON `llm-studies.blog.posts_dez_2024_emb`(text_embedding)
OPTIONS(distance_type='COSINE', index_type='IVF');
```

Query the same table

```bash
SELECT *
FROM
  VECTOR_SEARCH(
    TABLE blog.posts_dez_2024_emb,
    'text_embedding',
    (SELECT content, text_embedding FROM blog.posts_dez_2024_emb),
    'text_embedding',
    top_k => 2);
```

Query passing a text

```bash
SELECT query.query, base.post_title, base.post_url, base.statistics, round(cast(distance as float64), 2) as distance
FROM
  VECTOR_SEARCH(
    TABLE blog.posts_dez_2024_emb,
    'text_embedding',
    ( SELECT ml_generate_embedding_result, content AS query
  FROM ML.GENERATE_EMBEDDING(
  MODEL blog.text_emb,
  (SELECT 'teoria das formas de platão' AS content))
),
    top_k => 5)
order by distance desc
```

RAG

```bash
SELECT ml_generate_text_llm_result AS generated
FROM ML.GENERATE_TEXT(
  MODEL blog.text_model,
  (
    SELECT CONCAT(
      'Qual a ideia madre do texto: ',
      STRING_AGG(
        FORMAT("text title: %s, text abstract: %s", base.post_title, base.post_content),
        ',\n')
      ) AS prompt,
    FROM VECTOR_SEARCH(
      TABLE blog.posts_dez_2024_emb, 'text_embedding',
      (
        SELECT ml_generate_embedding_result, content AS query
        FROM ML.GENERATE_EMBEDDING(
          MODEL blog.text_emb,
         (SELECT 'teoria das formas de platão' AS content)
        )
      ),
    top_k => 5, options => '{"fraction_lists_to_search": 0.01}')
  ),
  STRUCT(600 AS max_output_tokens, TRUE AS flatten_json_output));
```

Posts voew

```bash
SELECT pc.classification, p.post_title, p.post_date, p.post_url, pc.justification, ps.summarization, p.post_content, p.post_labels, p.post_replies
FROM `llm-studies.blog.posts_dez_2024` p, `llm-studies.blog.posts_classification` pc, `llm-studies.blog.posts_summarization` ps
WHERE p.post_id = pc.post_id AND p.post_id = ps.post_id AND pc.post_id = ps.post_id
AND pc.baseline_id in (SELECT max(baseline_id) FROM `llm-studies.blog.model_baseline` WHERE task = 'classification')
AND ps.baseline_id in (SELECT max(baseline_id) FROM `llm-studies.blog.model_baseline` WHERE task = 'summarization')
```

# GCP

Insert posts into Big Query

```bash
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\create_post_table.py
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\insert_posts_into_bq.py
```

Post classification

```bash
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\create_model_baseline.py
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\create_classification_table.py
.venv\scripts\activate && .venv\Scripts\python.exe test\post_classificationt.py
.venv\scripts\activate && .venv\Scripts\python.exe src\post_classification.py
.venv\scripts\activate && jupyter notebook src\notebook\talk_with_the_blog.ipynb
```

Post summarization

```bash
.venv\scripts\activate && .venv\Scripts\python.exe test\post_summarizationt.py
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\create_summarization_table.py
.venv\scripts\activate && .venv\Scripts\python.exe src\post_summarization.py
.venv\scripts\activate && jupyter notebook src\notebook\talk_with_the_blog.ipynb
```

Talk with the data

```bash
.venv\scripts\activate && .venv\Scripts\python.exe -m streamlit run app\chat_app.py
```

```bash
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\upload_authors.py
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\insert_authors_into_bq.py
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\create_auth_table.py
```

# Processing

```bash
.venv\scripts\activate
jupyter notebook src\notebook\document_processing.ipynb
.venv\scripts\activate && .venv\Scripts\python.exe src\post_classification.py
.venv\scripts\activate && .venv\Scripts\python.exe src\post_summ.py
.venv\scripts\activate && .venv\Scripts\python.exe src\post_authors.py
.venv\scripts\activate && .venv\Scripts\python.exe src\post_arguments.py
```

# Test Dialogflow Integration

```bash
cd .\dialogflow-integrations\telegram
npm install
get-content .env | foreach {
    $name, $value = $_.split('=')
    set-content env:\$name $value
}
node server.js > node.log
```

# Build Dialogflow Integration

```bash
cd .\dialogflow-integrations\
get-content .env | foreach {
    $name, $value = $_.split('=')
    set-content env:\$name $value
}
gcloud builds submit --tag gcr.io/llm-studies/dialogflow-telegram
gcloud beta run deploy --image gcr.io/PROJECT_ID/dialogflow-telegram --service-account  --memory 1Gi --update-env-vars PROJECT_ID=, LOCATION=global, AGENT_ID=, LANG=pt,     TELEGRAM_TOKEN=, SERVER_URL=
```

# Looker

-[Report](https://lookerstudio.google.com/s/mxKD2HnuGI8)

# References

- [Blogger](https://developers.google.com/blogger)
- [Blogger APIs Client Library for Python](https://developers.google.com/blogger/docs/3.0/api-lib/python)
- [Dialogflow Integration](https://github.com/GoogleCloudPlatform/dialogflow-integrations/tree/master)
- [Telegram Integration for Dialogflow CX](https://github.com/GoogleCloudPlatform/dialogflow-integrations/tree/master/cx/telegram)
- [BotFather](https://web.telegram.org/k/#@BotFather)
- [Build history](https://console.cloud.google.com/cloud-build/builds?inv=1&invt=Abk6Jg&project=llm-studies&supportedpurview=project)
- [Generative AI overview](https://cloud.google.com/bigquery/docs/generative-ai-overview)
- [Build a basic LLM chat app](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)