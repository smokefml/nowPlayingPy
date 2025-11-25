import curses

COLOR_MAP = {
    "black": curses.COLOR_BLACK,
    "red": curses.COLOR_RED,
    "green": curses.COLOR_GREEN,
    "yellow": curses.COLOR_YELLOW,
    "blue": curses.COLOR_BLUE,
    "magenta": curses.COLOR_MAGENTA,
    "cyan": curses.COLOR_CYAN,
    "white": curses.COLOR_WHITE
}

def get_color_from_name(name):
    name = name.lower()
    return COLOR_MAP.get(name)

def hex_to_curses_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        return None
    r = int(hex_color[0:2], 16) * 1000 // 255
    g = int(hex_color[2:4], 16) * 1000 // 255
    b = int(hex_color[4:6], 16) * 1000 // 255
    return r, g, b

_next_custom_color = 20

def create_custom_color(hex_color):
    global _next_custom_color

    rgb = hex_to_curses_rgb(hex_color)
    if not rgb:
        return None

    if not curses.can_change_color():
        return None

    color_id = _next_custom_color
    _next_custom_color += 1

    curses.init_color(color_id, *rgb)
    return color_id

def resolve_color(color_str, fallback=curses.COLOR_WHITE):
    # 1. nombre standard
    color = get_color_from_name(color_str)
    if color is not None:
        return color

    # 2. hex tipo "#aabbcc"
    custom = create_custom_color(color_str)
    if custom is not None:
        return custom

    # 3. fallback
    return fallback

class ColorPairList:
    """Colores inicializados por curses"""
    def __init__(self, bg, error, alert, colors):
        self.background = bg
        self.error = error
        self.alert = alert
        self.foreground = 0
        self.header_color = 0
        self.separator_color = 0
        self.key_color = 0
        self.value_color = 0
        self.time_bar_color = 0
        self.volume_bar_color = 0
        self.empty_bar_color = 0
        for key, value in colors.items():
            setattr(self, key, value)

def init_color_pairs(colors_config):
    bg = resolve_color(colors_config["background"])

    pairs = {}
    pair_id = 3

    for key, color_str in colors_config.items():
        if key == "background":
            continue

        fg = resolve_color(color_str)
        curses.init_pair(pair_id, fg, bg)
        pairs[key] = curses.color_pair(pair_id)
        pair_id += 1

    return pairs, bg

def init_ui_colors(colors):
    curses.start_color()

    pairs, bg = init_color_pairs(colors)

    curses.init_pair(1,resolve_color('red'),bg)
    curses.init_pair(2,bg,resolve_color('white'))

    error_color = curses.color_pair(1)
    alert_color = curses.color_pair(2)

    color_list = ColorPairList(bg,error_color,alert_color,pairs)
    return color_list
