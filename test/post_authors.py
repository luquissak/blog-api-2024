import sys
from google.cloud import bigquery
import time
import json

import sys
sys.path.insert(1, './src')
import model_config
import prompts
import gcp.bq_queries as bq_queries


client = bigquery.Client()
MODEL_NAME = "gemini-1.5-flash-001"
TEMP = 0

def main(argv):
    print("starting...")
    rows = client.query_and_wait(bq_queries.query_a_post)
    for row in rows:
        print("post={}".format(row["post_title"]))
        print("content={}".format(row["post_content"]))
        modelResp = model_config.call_model(MODEL_NAME, TEMP,
                                                         prompts.authors_prompt,
                                                         row["post_content"],
                                                         print_raw_response=True,
                                                         )
        modelResp_json = json.loads(modelResp.text)

        print(f"modelResp_json: {modelResp_json["authors"]}")
        print(modelResp.finish_reason)
        print(modelResp.modelVersion)
        print(modelResp.totalTokenCount)

        authors_l = []
        for author in modelResp_json["authors"]:
            authors_l.append(author["author"])
        print(authors_l)


if __name__ == "__main__":
    main(sys.argv)