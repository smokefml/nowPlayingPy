import os
from .url_tools import extract_youtube_id, download_image

def get_cover(metadata):
    title = metadata["xesam:title"].value if "xesam:title" in metadata else ""
    picture_url = metadata["mpris:artUrl"].value if "mpris:artUrl" in metadata else None
    url = metadata["xesam:url"].value if "xesam:url" in metadata else None
    picture_local_uri = ""

    if "xesam:url" in metadata:
        if url and " - YouTube" in title:
            youtube_id = extract_youtube_id(url)
            if youtube_id:
                picture_url = 'https://img.youtube.com/vi/{}/hqdefault.jpg'.format(youtube_id)
        # ToDo otras condiciones para soprtar otros sitios?

    if picture_url:
        dlfolder = "/tmp/nowPlaying"
        try:
            picture_local_uri = download_image(picture_url, dlfolder)
        except Exception as e:
            #print(e)
            picture_local_uri = no_cover()
    else:
        picture_local_uri = no_cover()
    return picture_local_uri

def no_cover() -> str:
    return os.path.join(os.getcwd(), "nocover.jpg")
