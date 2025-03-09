query_all_posts = """
    SELECT blog_id, post_id, post_title, post_content
    FROM `llm-studies.blog.posts_dez_2024`
    """

query_new_posts_for_class = """
    SELECT blog_id, post_id, post_title, post_content
    FROM `llm-studies.blog.posts_dez_2024`
    WHERE post_id not in (SELECT post_id FROM `llm-studies.blog.posts_classification`)
    """

query_new_posts_for_summ = """
    SELECT blog_id, post_id, post_title, post_content
    FROM `llm-studies.blog.posts_dez_2024`
    WHERE post_id not in (SELECT post_id FROM `llm-studies.blog.posts_summarization`)
    """

query_a_post = """
    SELECT blog_id, post_id, post_title, post_content
    FROM `llm-studies.blog.posts_dez_2024`
    WHERE post_id = 1990325907199668907
    """