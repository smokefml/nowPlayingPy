import curses
import asyncio

from dbus_service.player_control import get_control
from ui.main_content import draw_conent
from ui.keys import key_catcher
from config.loader import get_config

async def async_main(stdscr):
    config = get_config()

    player_manager = await get_control()

    old_height = 0
    old_width = 0
    stdscr.nodelay(True)
    curses.curs_set(0)
    stdscr.clear()

    key_press = None

    while True:
        height, width = stdscr.getmaxyx()
        if height != old_height or width != old_width:
            old_height = height
            old_width = width
            player_manager.set_cover_should_refresh()
            stdscr.clear()

        key_press = await key_catcher(stdscr, player_manager)

        if key_press == 'quit':
            break

        draw_conent(stdscr, player_manager, key_press)

        await asyncio.sleep(0.01)
    player_manager.stop_update_loop()
    await player_manager.manager.disconnect()

def main_sync_wrapper(stdscr):
    asyncio.run(async_main(stdscr))

if __name__ == "__main__":
    curses.wrapper(main_sync_wrapper)
