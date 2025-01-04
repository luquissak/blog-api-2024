import sys
from datetime import datetime
from google.cloud import bigquery
import ast


table_id = "llm-studies.blog.posts_authors"
client = bigquery.Client()
log_date = datetime.now()


def insert_authors(authors_l, theme, area, url):
    print("Inserting %s..." % (url))

    rows_to_insert = [
        {"authors": authors_l, "theme": theme, "area": area, "url": str(url)}
    ]

    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        return 1
    else:
        print("Encountered errors while inserting rows: {}".format(errors))
        return 0


def main(argv):
    print("starting!")
    with open('files/posts_authors.csv', 'r') as the_file:
        total = 0
        for line in the_file:
            strip_line = line.rstrip()
            if strip_line == "authors|url":
                continue
            aut_dict = ast.literal_eval(strip_line.split("|")[0])
            authors_dict_l = aut_dict.get('authors')
            authors_l = []
            for author in authors_dict_l:
                authors_l.append(author.get('author'))
            theme = aut_dict.get('theme')
            area = aut_dict.get('philosophical area')
            if area == None: area = "Nenhuma"
            if theme == None: theme = "Nenhum"
            url = strip_line.split("|")[1]
            inserted = insert_authors(authors_l, theme, area, url)
            total = total + inserted
        return total

if __name__ == "__main__":
    total = main(sys.argv)
    print("Inseridos: %s" % total)

