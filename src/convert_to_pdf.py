from os import listdir
from os.path import isfile, join

path = "docao4"
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
for post in onlyfiles:
    print(post)

from docx2pdf import convert

convert(path)