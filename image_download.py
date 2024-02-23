import requests
from google.cloud import bigquery as bq
from pprint import pprint as pp

project = "imagebase-414802"
dataset = "imagebase"
label = "fantasy"

db_client = bq.Client(project=project)
db_table = f"{project}.{dataset}.{label}"


def get_items():
    """Get image headers from the database"""
    h_query = "id, title, prompt, url"
    return db_client.query(f"SELECT {h_query} FROM {db_table}").result()


for item in get_items():
    title = item["title"].replace(" ", "_")
    suffix = item["id"][:8]
    filename = f"/users/shared/images/{title}-{suffix}.png"
    print(filename)
    url = item["url"]
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)
