import zipfile
import os
import requests

print("""

    Sourcer Prepare
    1. Download /A-Soul-Database/PhotoSearch/releases/download/latest/Alphas.zip
    2. Unzip Alphas.zip

    Run: py prepare_data.py
"""
)
export_path = os.path.dirname(__file__)+ "/../Sync/Detect/"
with open(export_path+"Alphas.zip","wb") as f:
    chunk_size = 1024
    with requests.get("https://github.com/A-Soul-Database/PhotoSearch/releases/download/latest/Alphas.zip") as r:
        for chunk in r.iter_content(chunk_size=chunk_size):
            f.write(chunk)
            f.flush()

Alpha = zipfile.ZipFile(export_path+"Alphas.zip")
Alpha.extractall(export_path)
print("ok")