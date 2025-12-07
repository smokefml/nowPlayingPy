import os
from .url_tools import extract_youtube_id, download_image

def get_cover(metadata):
    title = metadata.get("xesam:title", "")
    picture_url = metadata.get("mpris:artUrl", None)
    url = metadata.get("xesam:url", None)
    picture_local_uri = ""

    if url:
        if "youtube.com" in url and title == "YouTube":
            picture_url = 'https://www.gstatic.com/youtube/img/web/maskable/logo_512x512.png'
        if "youtube" in url and " - YouTube" in title:
            youtube_id = extract_youtube_id(url)
            if youtube_id:
                picture_url = f'https://img.youtube.com/vi/{youtube_id}/hqdefault.jpg'
                if 'shorts' in url:
                    picture_url = f'https://i.ytimg.com/vi/{youtube_id}/frame0.jpg'
        # ToDo otras condiciones para soprtar otros sitios?
        if "x.com" in url and " / X" in title:
            picture_url = 'https://abs.twimg.com/responsive-web/client-web/icon-default-large.9ab12c3a.png'

    if picture_url:
        dlfolder = "/tmp/nowPlaying"
        try:
            # Puede devolver None sin fallar!
            picture_local_uri = download_image(picture_url, dlfolder)
        except Exception as e:
            #print(e)
            picture_local_uri = no_cover()
    
    if not picture_local_uri:
        return no_cover()

    return picture_local_uri
def no_cover() -> str:
    return os.path.join(os.getcwd(), "nocover.jpg")
