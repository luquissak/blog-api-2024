import sys
from dotenv import load_dotenv
from google.cloud import bigquery
import time
import prompts
import model_config
import json
import baseline
import gcp.bq_inserts as bq_inserts
import gcp.bq_queries as bq_queries

client = bigquery.Client()
TASK = "ner"
MODEL_NAME = "gemini-1.5-flash"
TEMP = 0


def main(argv):
    print("starting...")
    baselineId = baseline.create_baseline(client,
        TASK, prompts.authors_prompt, MODEL_NAME, TEMP)
    rows = client.query_and_wait(bq_queries.query_new_posts_for_authors)
    print(f"rows to be checked... {rows.total_rows}")
    for row in rows:
        print("post={}".format(row["post_title"]))
        modelResp = model_config.call_model(MODEL_NAME, TEMP,
                                            prompts.authors_prompt,
                                            row["post_content"],
                                            print_raw_response=False,
                                            )
        modelResp_json = json.loads(modelResp.text)
        authors = modelResp_json["authors"]
        authors_l = []
        for author in modelResp_json["authors"]:
            authors_l.append(author["author"])
        print(f"authors={authors_l}")
        bq_inserts.insert_authors(client, row["blog_id"], row["post_id"], baselineId, authors_l,
                                         modelResp.modelVersion, modelResp.totalTokenCount, modelResp.safetyRatings, modelResp.finish_reason)
        time.sleep(30)


if __name__ == "__main__":
    main(sys.argv)
