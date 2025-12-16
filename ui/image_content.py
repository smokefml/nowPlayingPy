from tools.system_commands import kitty_icat, kitty_icat_clear
from config.loader import get_config

def draw_cover(cover, should_refresh, refreshed):
    """
    Llama a dibujar la imagen de portada en el path, segun la condicion en la
    tupla (path,condicion) y, si se realizó la acción, llama al callback refreshed()
    """
    if should_refresh:
        try:
            draw_picture(cover)
            refreshed()
        except:
            return

def draw_picture(uri: str):
    """
    Dibuja la imagen en la ubicacion provista, el metodo y tamaño de presentación
    dependen de la configuración
    """
    config = get_config()
    method = config.ui.cover.method
    size = config.ui.cover.size
    if method == 'icat':
        kitty_icat_clear()
        kitty_icat(uri,2,1,size,size)

def clear_picture():
    """
    Borra la imagen de la pantalla, dependiendo del metodo configurado
    """
    config = get_config()
    method = config.ui.cover.method
    if method == 'icat':
        kitty_icat_clear()
