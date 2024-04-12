from os import listdir
from knimeParser import Parser
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

workflows = listdir("workflows")
with tqdm(total=len(workflows)) as pbar:
    with ThreadPoolExecutor() as executor:
        for future in as_completed([executor.submit(Parser, "workflows/" + filename) for filename in workflows]):
            pbar.update(1)
