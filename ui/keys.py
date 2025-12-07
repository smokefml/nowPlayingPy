import asyncio
import curses

async def key_catcher(win: curses.window, player_manager):
    actions = {
        "play_pause": {
            "cb": player_manager.play_pause,
            "keycode": ord(' ')
            },
        "next_track": {
            "cb": player_manager.next_track,
            "keycode": ord('n')
            },
        "previous_track": {
            "cb": player_manager.previous_track,
            "keycode": ord('p')
            },
        "seek_b5s": {
            "cb": player_manager.seek_b5s,
            "keycode": ord('a')
            },
        "seek_f5s": {
            "cb": player_manager.seek_f5s,
            "keycode": ord('d')
            },
        "quit": {
            "cb": lambda : 'quit',
            "keycode": ord('q')
            }
    }

    key = win.getch()

    if key == curses.ERR:
        return None

    for action_name, action_props in actions.items():
        if key == action_props.get('keycode'):
            callback = action_props.get('cb')

            if asyncio.iscoroutinefunction(callback):
                return await callback()

            return callback()

    return key
