from os import listdir
from os.path import isfile, join
from spire.doc import *
from spire.doc.common import *


path = "docs/posts/docx/"
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
print(onlyfiles)

for post in onlyfiles:
    print(post)

from docx2pdf import convert

convert(path)