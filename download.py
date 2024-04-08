from requests import Session
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

session = Session()
session.mount('https://', HTTPAdapter(max_retries=Retry(total=10000, status_forcelist=tuple(range(401, 600)))))


def download_file(data):
    file_path = "workflows/" + data["title"] + ".knwf"
    file_url = "https://api.hub.knime.com/repository" + data["pathToResource"] + ":data"
    file_content = session.get(file_url).content
    with open(file_path, mode="wb") as file:
        file.write(file_content)


workflows1 = session.get("https://api.hub.knime.com/search?type=Workflow&limit=10000&sort=maxKudos").json()["results"]
workflows2 = session.get("https://api.hub.knime.com/search?type=Workflow&limit=10000&sort=minKudos").json()["results"]
json_data = workflows2 + workflows1

with tqdm(total=len(json_data)) as pbar:
    with ThreadPoolExecutor(max_workers=5000) as executor:
        for future in as_completed([executor.submit(download_file, data) for data in json_data]):
            pbar.update(1)
