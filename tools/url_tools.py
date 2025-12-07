from urllib.parse import urlparse, parse_qs
import os
import hashlib
import requests

from .picture_tools import verify_image

def extract_youtube_id(url: str) -> str | None:
    parsed = urlparse(url)

    # Caso 1: youtube.com/watch?v=ID
    if parsed.hostname and "youtube" in parsed.hostname:
        qs = parse_qs(parsed.query)
        if "v" in qs:
            return qs["v"][0]

    # Caso 2: youtu.be/ID
    if parsed.hostname and "youtu.be" in parsed.hostname:
        # path arranca con "/", lo sacamos
        return parsed.path.lstrip("/")

    # Caso 3: youtube.com/shorts/ID
    if parsed.hostname and "shorts" in parsed.path:
        # path arranca con "shorts/", lo sacamos
        return parsed.path.lstrip("shorts/")

    return None

def download_image(url: str, folder="/tmp/nowPlaying") -> str | None:
    os.makedirs(folder, exist_ok = True)

    h = hashlib.sha1(url.encode()).hexdigest()
    dest_path = os.path.join(folder, h)

    if os.path.exists(dest_path):
        return dest_path

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        with open(dest_path, "wb") as f:
            f.write(r.content)
            f.close()
        # Checkear si la imagen es valida y cuadrada
        if verify_image(dest_path):
            return dest_path
        else:
            return None
    except Exception as e:
        #print("Error al descargar la imagen: ", e)
        return None
