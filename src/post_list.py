import os
import sys
from dotenv import load_dotenv
from datetime import datetime
from oauth2client import client
from googleapiclient import sample_tools

load_dotenv()
BLOG_ID = os.getenv('BLOG_ID')
print("BLOG_ID", BLOG_ID)

today = datetime.today().strftime('%Y%m%d') + "-"


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

    with open("files/"+today+"posts_list.csv", "a", encoding="utf-8") as the_file:
        the_file.write("name|title|url\n")
        for blog in thisusersblogs["items"]:
            print("The posts for %s:" % blog["name"])
            request = posts.list(blogId=blog["id"])
            while request != None:
                posts_doc = request.execute()
                if "items" in posts_doc and not (posts_doc["items"] is None):
                    for post in posts_doc["items"]:
                        print("  %s (%s)" % (post["title"], post["url"]))
                        the_file.write(blog["name"]+"|" +
                                       post["title"]+"|"+post["url"]+"\n")
                request = posts.list_next(request, posts_doc)


if __name__ == "__main__":
    main(sys.argv)
