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
```

4. Google Setup

```bash
gcloud auth login
gcloud components update
gcloud auth application-default login
gcloud config set project llm-studies
gcloud auth application-default set-quota-project llm-studies
gcloud auth list
gcloud config list
```

# Build and Test
```bash
$env:GOOGLE_APPLICATION_CREDENTIALS="credentials\client_secret_129125337363-uci7et766rno47m5p4m2tfukr8b3d1dd.apps.googleusercontent.com.json"
.venv\scripts\activate && .venv\Scripts\python.exe src\post_list.py
#--noauth_local_webserver
```
# References
- [Blogger](https://developers.google.com/blogger)
- [Blogger APIs Client Library for Python](https://developers.google.com/blogger/docs/3.0/api-lib/python)
