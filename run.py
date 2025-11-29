import curses
import asyncio

from dbus_service.player_control import get_control
from ui.main_content import draw_conent
from ui.image_content import clear_picture
from config.loader import get_config

MIN_WIDTH = 80
MIN_HEIGHT = 22

async def async_main(stdscr):
    config = get_config()

    player_manager = await get_control()

    cover, should_refresh = player_manager.get_cover_path()

    old_height = 0
    old_width = 0
    stdscr.nodelay(True)
    curses.curs_set(0)
    stdscr.clear()

    while True:
        height, width = stdscr.getmaxyx()
        if height != old_height or width != old_width:
            old_height = height
            old_width = width
            player_manager.set_cover_should_refresh()
            stdscr.clear()

        if height < MIN_HEIGHT or width < MIN_WIDTH:
            if should_refresh:
                clear_picture()
            stdscr.addstr(2, 2, f"Terminal Size: {width}x{height}",
                          config.ui.colors.table.alert)
            stdscr.addstr(4, 2, "Terminal too small!",
                          config.ui.colors.table.error)
            stdscr.refresh()
        else:
            draw_conent(stdscr, player_manager)

        key = stdscr.getch()
        if key == ord(' '):
            await player_manager.play_pause()
        elif key == ord('n'):
            await player_manager.next_track()
        elif key == ord('p'):
            await player_manager.previous_track()
        elif key == ord('a'):
            await player_manager.seek_b5s()
        elif key == ord('d'):
            await player_manager.seek_f5s()
        elif key == ord('q'):
            break

        await asyncio.sleep(0.01)
    await player_manager.manager.disconnect()

def main_sync_wrapper(stdscr):
    asyncio.run(async_main(stdscr))

if __name__ == "__main__":
    curses.wrapper(main_sync_wrapper)
