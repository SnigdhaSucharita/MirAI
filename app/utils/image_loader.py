import requests
import tempfile
import os

def download_image(image_url: str) -> str:
    response = requests.get(image_url, stream=True, timeout=10)
    response.raise_for_status()

    suffix = os.path.splitext(image_url)[-1] or ".jpg"

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    for chunk in response.iter_content(8192):
        tmp.write(chunk)
    tmp.close()

    return tmp.name
