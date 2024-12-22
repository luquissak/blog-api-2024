from os import listdir
from os.path import isfile, join
from spire.doc import *
from spire.doc.common import *


path = "docs/posts/"
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
print(onlyfiles)

for post in onlyfiles:
    print(post)
    document = Document()
    document.LoadFromFile(path+post)
    document.SaveToFile(path+"pdf/"+post.replace("docx","pdf"), FileFormat.PDF)
    document.Close()