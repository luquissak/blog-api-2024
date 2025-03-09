
def create_baseline(client, task, prompt, model_name, temp):
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
    VALUES ({baselineId}, "{task}", CURRENT_DATETIME(), "{prompt}", "{model_name}", {temp})
    """
    client.query_and_wait(query)
    return baselineId