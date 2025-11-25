import json
import curses
from dataclasses import asdict
from .schema import Config, AppConfig, UIConfig, CoverConfig, SeparatorConfig, BarsConfig, ColorsConfig
from tools.color_tools import init_ui_colors

CONFIG = None

def _load_partial(obj_class, data_dict):
    """Carga valores que existan, deja defaults para los que falten."""
    kwargs = {}
    for field in obj_class.__dataclass_fields__:
        if field in data_dict:
            value = data_dict[field]
        else:
            continue

        # si el valor es un dict y el campo es otra dataclass → procesarlo recursivamente
        field_type = obj_class.__dataclass_fields__[field].type
        if hasattr(field_type, "__dataclass_fields__") and isinstance(value, dict):
            kwargs[field] = _load_partial(field_type, value)
        else:
            kwargs[field] = value

    return obj_class(**kwargs)

def load_config(path="config.json"):
    with open(path, "r") as f:
        data = json.load(f)

    config = _load_partial(Config, data)

    # inicializar colores según config.colors
    color_table = init_ui_colors(asdict(config.ui.colors))
    config.ui.colors.table = color_table

    if config.ui.separator.character.lower() == 'default':
        config.ui.separator.char = curses.ACS_HLINE
    elif len(config.ui.separator.character) != 1:
        config.ui.separator.char = ' '
    else:
        config.ui.separator.char = config.ui.separator.character

    if config.ui.bars.character.lower() == 'default':
        config.ui.bars.char = curses.ACS_HLINE
    elif len(config.ui.bars.character) != 1:
        config.ui.bars.char = ' '
    else:
        config.ui.bars.char = config.ui.separator.character


    return config

def get_config():
    global CONFIG
    if CONFIG is None:
        CONFIG = load_config()
    return CONFIG
