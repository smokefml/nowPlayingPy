import curses
from config.loader import get_config

_osd_frames = 0
_old_action = None

actions = {
    "paused": [
        "    ▄             ",
        "    ██▄           ",
        "    ████▄         ",
        "    ██████▄       ",
        "    ████████▄     ",
        "    ██████████    ",
        "    ████████▀     ",
        "    ██████▀       ",
        "    ████▀         ",
        "    ██▀           ",
        "    ▀             "
    ],
    "playing": [
        "                  ",
        "    ██      ██    ",
        "    ██      ██    ",
        "    ██      ██    ",
        "    ██      ██    ",
        "    ██      ██    ",
        "    ██      ██    ",
        "    ██      ██    ",
        "    ██      ██    ",
        "    ██      ██    ",
        "                  "
    ],
    "next_track": [
        "                  ",
        "    █▄      ██    ",
        "    ███▄    ██    ",
        "    █████▄  ██    ",
        "    ███████▄██    ",
        "    ██████████    ",
        "    ███████▀██    ",
        "    █████▀  ██    ",
        "    ███▀    ██    ",
        "    █▀      ██    ",
        "                  "
    ],
    "seek_f5s": [
        "                  ",
        " █▄     █▄        ",
        " ███▄   ███▄      ",
        " █████▄ █████▄    ",
        " ██████████████▄  ",
        " ████████████████ ",
        " ██████████████▀  ",
        " █████▀ █████▀    ",
        " ███▀   ███▀      ",
        " █▀     █▀        ",
        "                  "
    ],
    "previous_track": [
        "                  ",
        "    ██      ▄█    ",
        "    ██    ▄███    ",
        "    ██  ▄█████    ",
        "    ██▄███████    ",
        "    ██████████    ",
        "    ██▀███████    ",
        "    ██  ▀█████    ",
        "    ██    ▀███    ",
        "    ██      ▀█    ",
        "                  "
    ],
    "seek_b5s": [
        "                  ",
        "        ▄█     ▄█ ",
        "      ▄███   ▄███ ",
        "    ▄█████ ▄█████ ",
        "  ▄██████████████ ",
        " ████████████████ ",
        "  ▀██████████████ ",
        "    ▀█████ ▀█████ ",
        "      ▀███   ▀███ ",
        "        ▀█     ▀█ ",
        "                  "
    ]
}

def draw_osd(win: curses.window, action):
    global _osd_frames
    global _old_action
    if action in actions.keys():
        _osd_frames = 100
        _old_action = action
    if _osd_frames == 0:
        _old_action = None
        return
    height, width = win.getmaxyx()
    config = get_config()
    logo = actions[_old_action]
    ox = int(width / 2) - int(len(logo[0]) / 2)
    oy = int(height / 2) - int(len(logo) / 2)
    i = 0

    for line in logo:
        win.addstr(oy + i, ox, line, config.ui.colors.table.header_color)
        i += 1

    _osd_frames = _osd_frames - 1

    win.refresh()
