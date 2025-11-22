import curses
import json
from .color_tools import init_ui_colors

def config_loader():
    with open('config.json', 'r') as f:
        config = json.load(f)

    default_char = curses.ACS_HLINE

    # app options
    favorite_player = config["app"]["favorite_player"]
    # ui options
    size, method, position = config["ui"]["cover"].values()
    draw_borders = config["ui"]["draw_borders"]
    separator_char_cfg = config["ui"]["separator"]["character"]
    separator_length = config["ui"]["separator"]["length"]
    bar_char_cfg = config["ui"]["bars"]["character"]
    time_bar_length = config["ui"]["bars"]["position_length"]
    volume_bar_length = config["ui"]["bars"]["volume_length"]
    nocolor = config["ui"]["no_colors"]

    if separator_char_cfg.lower() == "default":
        separator_char = default_char
    else:
        separator_char = separator_char_cfg
    if bar_char_cfg.lower() == "default":
        bar_char = default_char
    else:
        bar_char = bar_char_cfg
    # inicializar colores
    pairs, bg = init_ui_colors(config)

    return {
            "favorite_player": favorite_player,
            "cover_size": size,
            "cover_method": method,
            "cover_position": position,
            "draw_borders": draw_borders,
            "nocolor": nocolor,
            "base_bg": bg,
            "ui_elements": {
                "base_color": pairs["foreground"],
                "header_color": pairs["header_color"],
                "separator_color": pairs["separator_color"],
                "key_color": pairs["key_color"],
                "value_color": pairs["value_color"],
                "time_bar_color": pairs["time_bar_color"],
                "volume_bar_color": pairs["volume_bar_color"],
                "empty_bar_color": pairs["empty_bar_color"],
                "separator_length": separator_length,
                "separator_char": separator_char,
                "bar_char": bar_char,
                "key_indent": 2,
                "time_bar_length": time_bar_length,
                "volume_bar_length": volume_bar_length
                }
            }
