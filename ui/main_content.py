import curses

from config.loader import get_config
from dbus_service.player_control import PlayBackControl
from ui.text_content import draw_info
from ui.image_content import draw_picture

def draw_conent(main_win: curses.window, player: PlayBackControl):
    """
    Maneja la presentacion de todo el contenido en la ventana principal main_win
    """
    config = get_config()
    info_column = config.ui.cover.size + 3
    draw_borders = config.ui.draw_borders
    height, width = main_win.getmaxyx()
    infowin = curses.newwin(height, width - info_column, 0, info_column)
    coverwin = curses.newwin(height, info_column, 0, 0)
    if draw_borders:
        infowin.border(
            curses.ACS_VLINE, curses.ACS_VLINE,     # Lados izquierdo y derecho
            curses.ACS_HLINE, curses.ACS_HLINE,     # Lados superior e inferior
            curses.ACS_TTEE, curses.ACS_URCORNER,   # Esquinas superior izq/der
            curses.ACS_BTEE, curses.ACS_LRCORNER    # Esquinas inferior izq/der
        )
        coverwin.border(
            curses.ACS_VLINE, ' ',
            curses.ACS_HLINE, curses.ACS_HLINE,
            curses.ACS_ULCORNER, curses.ACS_HLINE,
            curses.ACS_LLCORNER, curses.ACS_HLINE
        )
        coverwin.addch(int(info_column / 2), 0, curses.ACS_LTEE)
        infowin.addch(int(info_column / 2), 0, curses.ACS_RTEE)
        coverwin.hline(int(info_column / 2), 1, curses.ACS_HLINE, info_column - 1)
    infowin.bkgd(' ', config.ui.colors.table.foreground)
    coverwin.bkgd(' ', config.ui.colors.table.foreground)
    coverwin.refresh()

    draw_info(infowin, player.get_info())

    cover, should_refresh = player.get_cover_path()
    if should_refresh:
        draw_picture(cover)
        player.set_cover_refreshed()
