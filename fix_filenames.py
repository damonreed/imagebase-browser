from google.cloud import bigquery as bq
from google.cloud import storage as gcs
from pprint import pprint as pp

project = "imagebase-414802"
dataset = "imagebase"
bucket = "nomadia-org-imagebase"
label = "fantasy"

db_client = bq.Client(project=project)
gcs_client = gcs.Client()
db_table = f"{project}.{dataset}.{label}"


def get_items():
    """Get image headers from the database"""
    h_query = "id, url"
    return db_client.query(f"SELECT {h_query} FROM {db_table}").result()


def rename_blob(bucket_name, blob_name, new_name):
    """Renames a blob."""
    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    new_blob = bucket.rename_blob(blob, new_name)

    print(f"Blob {blob.name} renamed to {new_blob.name}")


# Iterate over rows, check if it ends in .png
# If it does, skip to the next row
# If it doesn't, update the filename the url field in the database
for item in get_items():
    url = item["url"]
    if ".png" in url:
        print(f"Skipping {url}")
        continue
    else:
        print(f"Updating {url}")
        item_id = item["id"]
        new_url = url + ".png"
        new_blob_name = f"{label}/{item_id}.png"
        print(f"New url: {new_url}")
        print(f"Item id: {item_id}")
        print(f"New blob name: {new_blob_name}")
        query = f"""
        UPDATE {db_table}
        SET url = "{new_url}"
        WHERE id = "{item_id}"
        """
        print(f"Query: {query}")
        db_client.query(query).result()
        print(f"Updated URL for {item_id} to {new_url}")
        print(
            f"Renaming gc://{bucket}/{label}/{item_id} to gc://{bucket}/{new_blob_name}"
        )
        rename_blob(bucket, f"{label}/{item_id}", new_blob_name)
        print(f"Renamed {item_id} to {label}/{item_id}")
        print(f"Done with {item_id}")
        print("-----")
        # end after one iteration
