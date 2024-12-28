import sys
from datetime import datetime
from google.cloud import bigquery
from googleapiclient import sample_tools
import html2text


date_format = '%d/%m/%Y'

table_id = "llm-studies.blog.posts_dez_2024"
client = bigquery.Client()
log_date = datetime.now()


def get_post_date(post):
    try:
        return datetime.strptime(
            post["published"], '%Y-%m-%dT%H:%M:%S-03:00').date().strftime('%d/%m/%Y')
    except:
        return datetime.strptime(
            post["published"], '%Y-%m-%dT%H:%M:%S-02:00').date().strftime('%d/%m/%Y')


def insert_post(blogId, post):
    print("Starting...")

    blog_id = blogId
    post_id = post["id"]
    post_date = get_post_date(post)
    post_wday = ""
    post_url = post["url"]
    post_title = post["title"]
    post_content_html = html2text.html2text(post["content"])
    post_content = post["content"]
#    post_replies = post["replies"]
    post_labels = post["labels"]

    print("%s (%s)..." % (post_title, post_date))

    rows_to_insert = [
        {"blog_id": blog_id, "post_id": post_id, "log_date": str(log_date), "post_date": str(post_date), "post_wday": post_wday, "post_url": post_url,
            "post_title": post_title, "post_content_html": post_content_html, "post_content": post_content
            , 
            #"post_replies": post_replies, 
            "post_labels": post_labels}
    ]

    # Make an API request.
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))


def main(argv):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv,
        "blogger",
        "v3",
        __doc__,
        __file__,
        scope="https://www.googleapis.com/auth/blogger",
    )
    print("logged!")

    users = service.users()
    thisuser = users.get(userId="self").execute()
    print("This user's display name is: %s" % thisuser["displayName"])
    blogs = service.blogs()
    thisusersblogs = blogs.listByUser(userId="self").execute()
    for blog in thisusersblogs["items"]:
        print("The blog named '%s' is at: %s" % (blog["name"], blog["url"]))

    posts = service.posts()

    for blog in thisusersblogs["items"]:
        print("The posts for %s:" % blog["name"])
        blogId = blog["id"]
        request = posts.list(blogId=blogId)
        while request != None:
            posts_doc = request.execute()
            if "items" in posts_doc and not (posts_doc["items"] is None):
                for post in posts_doc["items"]:
                    insert_post(blogId, post)
                    exit()
            request = posts.list_next(request, posts_doc)


if __name__ == "__main__":
    main(sys.argv)
