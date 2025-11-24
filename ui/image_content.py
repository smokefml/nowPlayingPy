import sys
sys.path.append("..")

from tools.system_commands import kitty_icat, kitty_icat_clear

def draw_picture(uri: str, method: str, size: int):
    if method == 'icat':
        kitty_icat_clear()
        kitty_icat(uri,2,1,size,size)

def clear_picture(method: str):
    if method == 'icat':
        kitty_icat_clear()
