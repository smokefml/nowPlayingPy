import asyncio
import curses
from config.loader import get_config

_osd_frames = 0
_old_action = None



def volup_acn(volume):
    if not volume:
        return []
    return [
        f"                   {int(volume * 100)}   Vol + >           ",
        "                                            ",
    ] + vol_glyph(volume)

def voldn_acn(volume):
    if not volume:
        return []
    return [
        f"         < - Vol   {int(volume * 100)}                     ",
        "                                            ",
    ] + vol_glyph(volume)

def vol_glyph(volume):
    length = 40
    full = int(length * volume)
    empty = length - full
    bar1 = '█' * full
    bar2 = '▄' * empty
    shade = '▄█'

    return [
            f" {' ' * full} ▄{' ' * empty} ",
            f' {bar1}{shade}{bar2} ',
            f" {' ' * full} █{' ' * empty} "
    ]

def draw_osd(win: curses.window, info, action):
    global _osd_frames
    global _old_action

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
        ],
        "vol+": volup_acn(info.volume),
        "vol-": voldn_acn(info.volume)
    }

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
