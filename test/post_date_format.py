import sys
import os
from dotenv import load_dotenv
from googleapiclient import sample_tools
from docx import Document
import html2text
from datetime import datetime

load_dotenv()
BLOG_ID = os.getenv('BLOG_ID')
print("BLOG_ID", BLOG_ID)


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

    document = Document()

    for blog in thisusersblogs["items"]:
        print("The posts for %s:" % blog["name"])
        request = posts.list(blogId=blog["id"])
        while request != None:
            posts_doc = request.execute()
            if "items" in posts_doc and not (posts_doc["items"] is None):
                for post in posts_doc["items"]:
                    print("%s ..." % (post["title"]))

#                    %Y-%m-%dT17:25:00-03:00
                    post_day = datetime.strptime(post["published"], '%Y-%m-%dT%H:%M:%S-03:00').date()
                    print(post_day.strftime('%d/%m/%Y'))
                    exit()
            request = posts.list_next(request, posts_doc)


if __name__ == "__main__":
    main(sys.argv)
