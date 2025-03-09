import sys
from dotenv import load_dotenv
from google.cloud import bigquery
import time
import prompts
import model_config
import json

client = bigquery.Client()
MODEL_NAME = "gemini-1.5-flash"
TEMP = 0

def main(argv):
    print("starting...")
    query = """
    SELECT blog_id, post_id, post_title, post_content
    FROM `llm-studies.blog.posts_dez_2024`
    WHERE post_id = 1990325907199668907
    """
    rows = client.query_and_wait(query)
    for row in rows:
        print("post={}".format(row["post_title"]))
        modelResp = model_config.call_model(MODEL_NAME, TEMP,
                                                         prompts.classification_prompt,
                                                         row["post_content"],
                                                         print_raw_response=False,
                                                         )
        modelResp_json = json.loads(modelResp.text)

        print(modelResp_json["category"])
        print(modelResp_json["justification"])
        print(modelResp.modelVersion)
        print(modelResp.totalTokenCount)
        time.sleep(30)


if __name__ == "__main__":
    main(sys.argv)