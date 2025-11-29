"""
Manages all the text display
"""

import random
import re
import string
import curses
import nerdfonts as nf

from config.loader import get_config

_old_title = ""
_anim_cicles = 0

extra_icons = {
    "play_pause":  '󰐎',
    "volume_crossed": '',
    "music_note": '󰎇',
    "music_user": '󰠃',
    "cd": '󰀥',
    "music_clock": '󱫜',
    "repeat": '󰑖',
    "repeat_off": '󰑗',
    "repeat_once": '󰑘',
    "shuffle": '󰒟',
    "shuffle_off": '󰒞'
}

def chop_string_smart(s: str, max_len: int):
    """
    Corta una cadena en fragmentos de longitud máxima max_len, 
    priorizando los cortes en espacios o signos de puntuación.
    """
    chunks = []
    start_index = 0
    s_len = len(s)

    while start_index < s_len:
        # Caso 1: El resto de la cadena cabe en un solo fragmento.
        if s_len - start_index <= max_len:
            chunks.append(s[start_index:].strip())
            break

        # Caso 2: El segmento actual es más largo que max_len.
        end_index = start_index + max_len
        segment = s[start_index:end_index]

        # Busca el último espacio o signo de puntuación en el segmento.
        # Usa r'[\s,.!?;:]' para incluir todos los espacios y puntuación comunes.
        match = re.search(r'[\s,.!?;:](?=[^\s,.!?;:]*$)', segment)

        if match:
            # Si se encuentra un punto de corte natural, corta allí.
            cut_point = start_index + match.start()
        else:
            # Si no se encuentra un punto de corte natural dentro del límite,
            # corta exactamente en max_len (para palabras muy largas).
            cut_point = end_index

        chunks.append(s[start_index:cut_point].strip())
        start_index = cut_point

    return chunks

def chop_string(s:str, lg:int):
    """
    Corta una cadena en fragmentos de longitud fija lg.
    """
    return [s[i:i+lg] for i in range(0, len(s), lg)]

def status_icon(status: str):
    """
    Devuelve un icono apropiado para el estado recibido.
    """
    if status == 'Playing':
        return nf.icons['fa_play']

    if status == 'Paused':
        return nf.icons['fa_pause']

    return nf.icons['fa_stop']

def volume_icon(volume: float):
    """
    Devuelve un icono apropiado para el nivel de volumen recibido.
    """
    if volume == 0.0:
        return nf.icons['fa_volume_off']
    if volume <= 0.6:
        return nf.icons['fa_volume_down']
    if volume > 0.6:
        return nf.icons['fa_volume_up']

    return extra_icons['volume_crossed']

def repeat_icon(repeat: str):
    if repeat == 'None':
        return extra_icons.get('repeat_off')
    if repeat == 'Track':
        return extra_icons.get('repeat_once')
    if repeat == 'Playlist':
        return extra_icons.get('repeat')

    return extra_icons.get('repeat_off')

def draw_loading_bar(window:curses.window, y:int, x:int, c,
                     tlen:int, fullp:float, attrf, attre):
    """
    Dibuja una barra de carga en la ventana window, posicion y,x, usando el
    caracter c, de longitud total tlen, de la cual fullp (0,0 a 1,0) esta lleno
    con atributos attrf para la parte llena y attre para la vacia
    """
    len_full = int(fullp * tlen)
    len_empty = int(tlen - len_full)
    window.hline(y, x, c, len_full, attrf)
    window.hline(y, x + len_full, c, len_empty, attre)

def draw_key_value(window:curses.window, y:int, x:int, vstr:str,
                   kicon='', kstr='', attrk=None, attrv=None):
    """
    Dibuja pares key: value, con icono, en la ventana window, posicion x,y,
    con los atributos attrk y attrv respectivamente
    """
    key_str = ''
    if kicon:
        key_str = key_str + kicon + "  "
    if kstr:
        key_str = key_str + kstr + ": "

    window.addstr(y, x, key_str, attrk)
    window.addstr(y, x + len(key_str), vstr, attrv)

def format_title_action(t: str):
    """
    Formatea titulo y action key para ciertos titulos muy largos
    generalmente util para web video players
    """
    if ' - YouTube' in t:
        title = t.replace(" - YouTube", "")
        action = f"{nf.icons['fa_youtube_play']}  YouTube: "
    elif ' / X' in t:
        title = t.replace(" / X", "")
        action = 'X  Browsing: '
    else:
        title = t
        action = f"{nf.icons['fa_film']}  Watching: "

    return title, action

def scramble_str(s: str, disable = False):
    """
    Scrambles string for animation purposes
    """
    if disable:
        return s

    rnd_str = ''.join(random.choices(string.ascii_letters + string.digits, k=len(s)))
    return rnd_str

def draw_info(window: curses.window, info):
    """
    Formatea y muestra la información recibida en el diccionario info,
    según los atributos en el diccionario ui_attr, en la ventada window.
    """
    config = get_config()
    colors = config.ui.colors.table
    sep_props = config.ui.separator
    bar_props = config.ui.bars
    key_indent = 2

    player = info.player
    title = info.title
    artist = info.artist
    album = info.album
    length = info.length
    position = info.position
    volume = info.volume
    status = info.status

    global _old_title
    global _anim_cicles

    if title != _old_title:
        _anim_cicles = 120
        _old_title = title

    #window.addstr(0,0, "cover: {}".format(album_art_path))

    # Separator
    window.hline(2, key_indent, sep_props.char, sep_props.length, colors.separator_color)

    # If no players
    if not player and not status:
        window.addstr(1, key_indent, f"{status_icon(status)}  Not Playing",
                      curses.color_pair(1) | curses.A_BOLD
                      )
        window.addstr(3, key_indent, f"{nf.icons['fa_exclamation_triangle']}  {info.note}",
                      colors.value_color | curses.A_BOLD
                      )

        window.refresh()
        return

    # Header
    window.addstr(1, key_indent, f"{status_icon(status)}  {status} {player}",
                  colors.header_color | curses.A_BOLD
                  )

    # key: value
    if title and not artist and not album:
        title, action = format_title_action(title)
        title_chunks = chop_string_smart(title, 32)
        window.addstr(3, key_indent, action, colors.key_color | curses.A_BOLD)
        i = 0
        for chunk in title_chunks:
            window.addstr(3 + i, key_indent + len(action),
                          scramble_str(chunk, _anim_cicles == 0), colors.value_color)
            if i >= 2:
                break
            i = i + 1
    else:
        draw_key_value(window, 3, key_indent, scramble_str(title, _anim_cicles == 0),
                       extra_icons.get('music_note'),
                       'Title', colors.key_color | curses.A_BOLD, colors.value_color)
        draw_key_value(window, 4, key_indent, scramble_str(artist, _anim_cicles == 0),
                       extra_icons.get('music_user'),
                       'Artist', colors.key_color | curses.A_BOLD, colors.value_color)
        draw_key_value(window, 5, key_indent, scramble_str(album, _anim_cicles == 0),
                       extra_icons.get('cd'),
                       'Album', colors.key_color | curses.A_BOLD, colors.value_color)

    draw_key_value(window, 7, key_indent,
                   f"{int(position/60):02d}:{int(position%60):02d} / " +
                   f"{int(length/60):02d}:{int(length%60):02d}",
                   extra_icons.get('music_clock'), '',
                   colors.key_color | curses.A_BOLD, colors.value_color)

    window.addstr(7, key_indent + 18,
                  f"{repeat_icon(info.repeat)}  " +
                  f"{extra_icons.get('shuffle') if info.shuffle else extra_icons.get('shuffle_off')}",
                  colors.key_color)

    draw_loading_bar(window, 8, key_indent + 3, bar_props.char, bar_props.position_length,
                     1 if length == 0 else position / length,
                     colors.time_bar_color, colors.empty_bar_color)

    if volume:
        draw_key_value(window,10,key_indent,f"{int(volume * 100)}%",
                       volume_icon(volume),'Volume',
                       colors.key_color | curses.A_BOLD, colors.value_color)

        draw_loading_bar(window, 11, key_indent + 3, bar_props.char,
                         bar_props.volume_length, volume,
                         colors.volume_bar_color, colors.empty_bar_color)

    if _anim_cicles > 0:
        _anim_cicles = _anim_cicles - 1

    window.refresh()
