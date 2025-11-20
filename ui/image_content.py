import sys
sys.path.append("..")

from tools.system_commands import kitty_icat

def draw_picture(uri: str, method: str, size: int):
    if method == 'icat':
        kitty_icat(uri,2,1,size,size)
