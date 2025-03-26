import datetime


def insert_classification(client, blogId, postId, baselineId, classification, justification, model_version, totalTokenCount, safetyRatings):

    rows_to_insert = [
        {"safety_ratings": safetyRatings, "total_token_count": totalTokenCount, "model_version": model_version,
         "classification": classification,
         "log_date": str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
         "baseline_id": baselineId,
         "post_id": postId,
         "blog_id": blogId,
         "justification": justification}
    ]
    errors = client.insert_rows_json(
        "llm-studies.blog.posts_classification", rows_to_insert)
    if errors != []:
        print("Encountered errors while inserting rows: {}".format(errors))
        exit()
    else:
        return 1

def insert_summarization(client, blogId, postId, baselineId, summarization, model_version, totalTokenCount, safetyRatings):

    rows_to_insert = [
        {"safety_ratings": safetyRatings, "total_token_count": totalTokenCount, "model_version": model_version,
         "summarization": summarization,
         "log_date": str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
         "baseline_id": baselineId,
         "post_id": postId,
         "blog_id": blogId,}
    ]
    errors = client.insert_rows_json(
        "llm-studies.blog.posts_summarization", rows_to_insert)
    if errors != []:
        print("Encountered errors while inserting rows: {}".format(errors))
        exit()
    else:
        return 1

def insert_authors(client, blogId, postId, baselineId, authors, model_version, totalTokenCount, safetyRatings, finish_reason):

    rows_to_insert = [
        {"safety_ratings": safetyRatings, "total_token_count": totalTokenCount, "model_version": model_version,
         "post_authors": authors,
         "log_date": str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
         "baseline_id": baselineId,
         "post_id": postId,
         "blog_id": blogId,
         "finish_reason": finish_reason}
    ]
    errors = client.insert_rows_json(
        "llm-studies.blog.posts_authors2", rows_to_insert)
    if errors != []:
        print("Encountered errors while inserting rows: {}".format(errors))
        exit()
    else:
        return 1
