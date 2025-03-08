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

# BQ Commands

Text Embeddings

```bash
bq mk --connection --location=us --project_id=llm-studies --connection_type=CLOUD_RESOURCE to-vertex-us-g
bq show --connection llm-studies.us.to-vertex-us-g
gcloud projects add-iam-policy-binding 129125337363 --member='serviceAccount:bqcx-129125337363-4se3@gcp-sa-bigquery-condel.iam.gserviceaccount.com' --role='roles/aiplatform.user' --condition=None
```

```
CREATE OR REPLACE MODEL `llm-studies.blog.text_emb`
REMOTE WITH CONNECTION `129125337363.us.to-vertex-us-g`
OPTIONS (ENDPOINT = 'text-embedding-004');
```

```
CREATE OR REPLACE TABLE `llm-studies.blog.posts_dez_2024_emb`
as
SELECT * FROM ML.GENERATE_TEXT_EMBEDDING(
   MODEL `llm-studies.blog.text_emb`,
   (SELECT post_content as content FROM `llm-studies.blog.posts_dez_2024`)
)
```

```
CREATE OR REPLACE VECTOR INDEX `llm-studies.blog.post_content_index`
ON `llm-studies.blog.posts_dez_2024_emb`(text_embedding)
OPTIONS(distance_type='COSINE', index_type='IVF');
```

```
SELECT *
FROM
  VECTOR_SEARCH(
    TABLE blog.posts_dez_2024_emb,
    'text_embedding',
    (SELECT content, text_embedding FROM blog.posts_dez_2024_emb),
    'text_embedding',
    top_k => 2);
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
.venv\scripts\activate && jupyter notebook src\notebook\classification_queries.ipynb
```

```bash
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\upload_class.py
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\load_class.py
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\upload_authors.py
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\insert_authors_into_bq.py
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\create_auth_table.py
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\upload_summ.py
#.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\load_summ.py
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\create_summ_table.py
.venv\scripts\activate && .venv\Scripts\python.exe src\gcp\insert_summ_into_bq.py
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
