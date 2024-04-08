import os
from zipfile import ZipFile
from knimeParser import Parser

for filename in os.listdir("workflows"):
    path = "workflows/" + filename
    with ZipFile(path) as zf:
        print(filename)
        p = Parser(path)