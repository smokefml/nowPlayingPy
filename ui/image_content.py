from tools.system_commands import kitty_icat, kitty_icat_clear
from config.loader import get_config

def draw_picture(uri: str):
    config = get_config()
    method = config.ui.cover.method
    size = config.ui.cover.size
    if method == 'icat':
        kitty_icat_clear()
        kitty_icat(uri,2,1,size,size)

def clear_picture():
    config = get_config()
    method = config.ui.cover.method
    if method == 'icat':
        kitty_icat_clear()
