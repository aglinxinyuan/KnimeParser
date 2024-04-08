import os
from zipfile import ZipFile
from xml.etree import ElementTree
from knimeParser import Parser

for filename in os.listdir("workflows"):
    path = "workflows/" + filename
    with ZipFile(path) as zf:
        res = any("Component Input" in namelist for namelist in zf.namelist())
        if not res:
            Parser(path)