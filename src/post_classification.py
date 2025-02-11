import sys
from dotenv import load_dotenv
from google.cloud import bigquery
import time
import prompts
import model_config
import datetime

client = bigquery.Client()
MODEL_NAME = "gemini-1.5-flash"
TEMP = 0


def create_baseline(task, prompt):
    client = bigquery.Client()
    query = f"""
    SELECT max(baseline_id) as baseline_id
    FROM `llm-studies.blog.model_baseline`
    """
    rows = client.query_and_wait(query)
    try:
        for row in rows:
            baselineId = row["baseline_id"] + 1
    except:
        baselineId = 1
    query = f"""
    INSERT INTO `llm-studies.blog.model_baseline` (baseline_id, task, log_date, prompt, model, temperature)
    VALUES ({baselineId}, "{task}", CURRENT_DATETIME(), "{prompt}", "{MODEL_NAME}", {TEMP})
    """
    client.query_and_wait(query)
    return baselineId


def insert_classification(blogId, postId, baselineId, classification, model_version, totalTokenCount, safetyRatings):

    rows_to_insert = [
        {"safety_ratings": safetyRatings, "total_token_count": totalTokenCount, "model_version": model_version,
         "classification": classification,
         "log_date": str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
         "baseline_id": baselineId,
         "post_id": postId,
         "blog_id": blogId}
    ]
    errors = client.insert_rows_json(
        "llm-studies.blog.posts_classification", rows_to_insert)
    if errors != []:
        print("Encountered errors while inserting rows: {}".format(errors))
        exit()
    else:
        return 1


def main(argv):
    print("starting...")
    baselineId = create_baseline(
        "classification", prompts.classification_prompt)
    query = """
    SELECT blog_id, post_id, post_title, post_content
    FROM `llm-studies.blog.posts_dez_2024`
    WHERE post_id not in (SELECT post_id FROM `llm-studies.blog.posts_classification`)
    """
    rows = client.query_and_wait(query)
    for row in rows:
        print("post={}".format(row["post_title"]))
        modelResp = model_config.call_model(MODEL_NAME, TEMP,
                                                         prompts.classification_prompt,
                                                         row["post_content"],
                                                         print_raw_response=False,
                                                         )
        insert_classification(row["blog_id"], row["post_id"], baselineId, modelResp.text,
                              modelResp.modelVersion, modelResp.totalTokenCount, modelResp.safetyRatings)
        time.sleep(30)


if __name__ == "__main__":
    main(sys.argv)
