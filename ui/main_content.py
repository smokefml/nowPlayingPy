import random
import string
import curses

from config.loader import get_config
from dbus_service.player_control import PlayBackControl
from ui.text_content import draw_info
from ui.image_content import draw_cover, clear_picture
from ui.osd import draw_osd

def draw_all_borders(rwin:curses.window, lwin:curses.window, swidth:int, draw=False):
    """
    Dibuja los bordes de ventana, si estan habilitados en la configuracion
    """
    if not draw:
        return
    rwin.border(
        curses.ACS_VLINE, curses.ACS_VLINE,     # Lados izquierdo y derecho
        curses.ACS_HLINE, curses.ACS_HLINE,     # Lados superior e inferior
        curses.ACS_TTEE, curses.ACS_URCORNER,   # Esquinas superior izq/der
        curses.ACS_BTEE, curses.ACS_LRCORNER    # Esquinas inferior izq/der
    )
    lwin.border(
        curses.ACS_VLINE, ' ',
        curses.ACS_HLINE, curses.ACS_HLINE,
        curses.ACS_ULCORNER, curses.ACS_HLINE,
        curses.ACS_LLCORNER, curses.ACS_HLINE
    )
    lwin.addch(int(swidth / 2), 0, curses.ACS_LTEE)
    rwin.addch(int(swidth / 2), 0, curses.ACS_RTEE)
    lwin.hline(int(swidth / 2), 1, curses.ACS_HLINE, swidth - 1)

def draw_conent(main_win: curses.window, player: PlayBackControl, action):
    """
    Maneja la presentacion de todo el contenido en la ventana principal main_win
    """
    # Config
    MIN_WIDTH = 80
    MIN_HEIGTH = 22
    config = get_config()
    info_column = config.ui.cover.size + 3
    draw_borders = config.ui.draw_borders
    height, width = main_win.getmaxyx()
    cover, should_refresh = player.get_cover_path()

    if height < MIN_HEIGTH or width < MIN_WIDTH:
        if should_refresh:
            clear_picture()
        main_win.addstr(2, 2, f"Terminal Size: {width}x{height}",
                        config.ui.colors.table.alert)
        main_win.addstr(4, 2, "Terminal too small!",
                          config.ui.colors.table.error)
        main_win.refresh()
        return

    # Definimos las ventanas
    infowin = curses.newwin(height, width - info_column, 0, info_column)
    coverwin = curses.newwin(height, info_column, 0, 0)
    # Dibujamos los bordes
    draw_all_borders(infowin,coverwin,info_column,draw_borders)
    # Color base de la ventana
    infowin.bkgd(' ', config.ui.colors.table.foreground)
    coverwin.bkgd(' ', config.ui.colors.table.foreground)

    #coverwin.addstr(int(info_column / 2) + 1, 2, f"size: {width}x{height}",
    #                random.choice(config.ui.colors.table))

    coverwin.refresh()
    # Dibujamos el contenido
    draw_info(infowin, player.get_info())
    draw_cover(cover, should_refresh, player.set_cover_refreshed)
    draw_osd(infowin, action)
