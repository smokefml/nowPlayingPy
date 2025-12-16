import curses

from dbus_service.bus_tasks import list_mpris_players
from dbus_service.player_control import get_control
from config.loader import get_config

async def show_players(win: curses.window, show=False):
    if show == False:
        return

    config = get_config()
    player_manager = await get_control()
    players = await list_mpris_players()

    win.clear()
    selected = 0
    while show:
        height, width = win.getmaxyx()
        key_indent = 2
        if config.ui.draw_borders:
            win.border()
        win.hline(2, key_indent, config.ui.separator.char,
                  config.ui.separator.length,
                  config.ui.colors.table.separator_color)
        win.addstr(1,key_indent,'  Available Players')
        y = 0
        for player in players:
            s_ind = ''
            attrs =  config.ui.colors.table.value_color
            if y == selected:
                s_ind = '> '
                attrs = config.ui.colors.table.key_color | curses.A_BOLD
            win.addstr(y + 3, key_indent,
                       f"{s_ind}{player.removeprefix('org.mpris.MediaPlayer2.')}   ",
                       attrs
                       )
            y += 1

        win.refresh()

        key = win.getch()
        if key == ord('w'):
            selected -= 1
            if selected < 0:
                selected = len(players) - 1
        if key == ord('s'):
            selected += 1
            if selected > len(players) - 1:
                selected = 0
        if key == ord('\n'):
            await player_manager.manager.swap_player(players[selected])
            show = False
        if key == ord('r'):
            show = False
