import sys
from datetime import datetime
from google.cloud import bigquery
import ast


table_id = "llm-studies.blog.posts_authors"
client = bigquery.Client()
log_date = datetime.now()


def insert_authors(authors_l, theme, area, url):
    print("Inserting...")

    print("%s (%s)..." % (url, theme))

    rows_to_insert = [
        {"authors": authors_l, "theme": theme, "area": area, "url": str(url)}
    ]

    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))


def main(argv):
    print("starting!")
    with open('files/posts_authors.csv', 'r') as the_file:
        for line in the_file:
            strip_line = line.rstrip()
            if strip_line == "authors|url":
                continue
            aut_dict = ast.literal_eval(strip_line.split("|")[0])
            authors_dict_l = aut_dict.get('authors')
            authors_l = []
            for author in authors_dict_l:
                print(author.get('author'))
                authors_l.append(author.get('author'))
            theme = aut_dict.get('theme')
            area = aut_dict.get('philosophical area')
            url = strip_line.split("|")[1]
            print(url)
            insert_authors(authors_l, theme, area, url)


if __name__ == "__main__":
    main(sys.argv)
