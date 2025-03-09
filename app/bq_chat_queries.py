
class BQ_chat_queries:
    def __new__(cls, *args, **kwargs):
        print("1. Create a new instance of bq_chat_queries.")
        return super().__new__(cls)

    def __init__(self, question):
        print("2. Initialize the new instance of bq_chat_queries.")
        self.question = question
        self.query_qa = f"""
            SELECT query.query, base.post_title as post_title, base.post_url, base.statistics, round(cast(distance as float64), 2) as distance
            FROM
            VECTOR_SEARCH(
                TABLE blog.posts_dez_2024_emb,
                'text_embedding',
                ( SELECT ml_generate_embedding_result, content AS query
            FROM ML.GENERATE_EMBEDDING(
            MODEL blog.text_emb,
            (SELECT '{self.question}' AS content))
            ),
                top_k => 5)
            order by distance desc
            """

    def __repr__(self) -> str:
        return f"{type(self).__name__}(x={self.question})"