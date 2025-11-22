import curses
import asyncio

from dbus_service.player_bus_connection import PlayerBusConnection
from tools.cover_tools import get_cover, no_cover
from tools.json_tools import config_loader
from ui.text_content import draw_info
from ui.image_content import draw_picture

MIN_WIDTH = 80
MIN_HEIGHT = 22

async def async_main(stdscr):
    config = config_loader()

    player_manager = PlayerBusConnection(config["favorite_player"])
    try:
        await player_manager.connect()
    except Exception as e:
        print(f"Ocurrió un problema al conectar con DBus: {e}")

    cover_size = config["cover_size"]
    cover_method = config["cover_method"]
    info_column = cover_size + 3
    draw_borders = config["draw_borders"]

    old_height = 0
    old_width = 0
    stdscr.nodelay(True)
    curses.curs_set(0)
    stdscr.clear()

    base_bg = config["base_bg"]
    ui_elements = config["ui_elements"]
    curses.init_pair(1, curses.COLOR_RED, base_bg)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    last_cover = ""

    while True:
        height, width = stdscr.getmaxyx()
        if height != old_height or width != old_width:
            old_height = height
            old_width = width
            stdscr.clear()

        try:
            player_identity = await player_manager.get_identity()
            meta = await player_manager.get_metadata()
            title = meta["xesam:title"].value
            artist = meta["xesam:artist"].value[0]
            album = meta["xesam:album"].value
            length = meta["mpris:length"].value/1000000 if "mpris:length" in meta else 0
            position_us = await player_manager.get_position()
            position = position_us/1000000
            status = await player_manager.get_status()
            volume = await player_manager.get_volume()
            cover = get_cover(meta)
        except Exception as e:
            player_identity = 'STOP'
            title = f"{e}"
            artist = 'STOP'
            album = 'STOP'
            length = 0
            position = 0
            status = 'STOP'
            volume = None
            cover = no_cover()

        playing_info = {
            "player": player_identity,
            "title": title,
            "artist": artist,
            "album": album,
            "cover_path": cover,
            "length": length,
            "position": position,
            "volume": volume,
            "status": status
        }

        if height < MIN_HEIGHT or width < MIN_WIDTH:
            stdscr.addstr(2, 2, f"Terminal Size: {width}x{height}", curses.color_pair(2))
            stdscr.addstr(4, 2, "Terminal too small!", curses.color_pair(1))
            stdscr.refresh()
        else:
            infowin = curses.newwin(height, width - info_column, 0, info_column)
            coverwin = curses.newwin(height, info_column, 0, 0)
            if draw_borders:
                infowin.border(
                    curses.ACS_VLINE, curses.ACS_VLINE,  # Lados izquierdo y derecho
                    curses.ACS_HLINE, curses.ACS_HLINE,  # Lados superior e inferior
                    curses.ACS_TTEE, curses.ACS_URCORNER, # Esquinas superior izq/der
                    curses.ACS_BTEE, curses.ACS_LRCORNER  # Esquinas inferior izq/der
                )
                coverwin.border(
                    curses.ACS_VLINE, ' ',  # Lados izquierdo y derecho
                    curses.ACS_HLINE, curses.ACS_HLINE,  # Lados superior e inferior
                    curses.ACS_ULCORNER, curses.ACS_HLINE, # Esquinas superior izq/der
                    curses.ACS_LLCORNER, curses.ACS_HLINE # Esquinas inferior izq/der
                )
                coverwin.addch(int(info_column / 2), 0, curses.ACS_LTEE)
                infowin.addch(int(info_column / 2), 0, curses.ACS_RTEE)
                coverwin.hline(int(info_column / 2), 1, curses.ACS_HLINE, info_column - 1)
            infowin.bkgd(' ', ui_elements['base_color'])
            coverwin.bkgd(' ', ui_elements['base_color'])
            coverwin.hline(int(info_column / 2), 1, curses.ACS_HLINE, info_column - 1)
            coverwin.refresh()
            draw_info(infowin, playing_info, ui_elements)
            if cover != last_cover:
                draw_picture(cover, cover_method, cover_size)
                last_cover = cover

        key = stdscr.getch()
        if key == ord(' '):
            await player_manager.play_pause()
        elif key == ord('n'):
            await player_manager.next_track()
        elif key == ord('p'):
            await player_manager.previous_track()
        elif key == ord('q'):
            break

        await asyncio.sleep(0.1)
    await player_manager.disconnect()

def main_sync_wrapper(stdscr):
    asyncio.run(async_main(stdscr))

if __name__ == "__main__":
    curses.wrapper(main_sync_wrapper)
