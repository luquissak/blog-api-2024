import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
BLOG_ID = os.getenv('BLOG_ID')
print("BLOG_ID", BLOG_ID)
KEY = os.getenv('KEY')

url = "https://www.googleapis.com/blogger/v3/blogs/"+BLOG_ID+"/posts/4141860721292182621/comments?key="+KEY

response = requests.request("GET", url, headers={}, data={})

json_obj = json.loads(response.text)

comments = "Comentários: "
i = 0
for comment in json_obj['items']:
    comments = comments + comment['content'] + "\n"
    i = i+1
print(comments, i)