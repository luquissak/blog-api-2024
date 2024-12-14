import os
import sys
from dotenv import load_dotenv
from oauth2client import client
from googleapiclient import sample_tools

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

if __name__ == "__main__":
    main(sys.argv)