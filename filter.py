import os
from knimeParser import Parser
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=300) as executor:
    for filename in os.listdir("workflows"):
        path = "workflows/" + filename
        executor.submit(Parser, path)