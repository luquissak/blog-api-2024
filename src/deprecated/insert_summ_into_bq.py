import sys
from datetime import datetime
from google.cloud import bigquery
import ast


table_id = "llm-studies.blog.posts_summ"
client = bigquery.Client()
log_date = datetime.now()


def insert_authors(summ, url):
    print("Inserting %s..." % (url))

    rows_to_insert = [
        {"summ": summ, "url": str(url)}
    ]
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        return 1
    else:
        print("Encountered errors while inserting rows: {}".format(errors))
        return 0


def main(argv):
    print("starting!")
    with open('files/posts_summ.csv', 'r') as the_file:
        total = 0
        for line in the_file:
            strip_line = line.rstrip()
            if strip_line == "summ|url":
                continue
            summ = strip_line.split("|")[0]
            url = strip_line.split("|")[1]
            try:
                inserted = insert_authors(summ, url)
            except:
                inserted = 0
            total = total + inserted
        return total

if __name__ == "__main__":
    total = main(sys.argv)
    print("Inseridos: %s" % total)

