"""
Esquema de configuracion de la aplicacion, con tipos de datos y valores por
defecto para cada opcion.
"""
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class CoverConfig:
    """
    Opciones de portada: ancho, metodo de presentacion y alineacion
    """
    size: int = 36
    method: str = "icat"
    position: str = "left"

@dataclass
class SeparatorConfig:
    """
    Opciones del separador bajo la cabecera: caracter y longitud
    """
    character: str = "default"
    length: int = 38

@dataclass
class BarsConfig:
    """
    Opciones de barras: Caracter, longitud de la barra de tiempo y de la de volumen
    """
    character: str = "default"
    position_length: int = 30
    volume_length: int = 20

@dataclass
class ColorsConfig:
    """
    Colores de los diferentes elementos de la UI, pueden ser estandar como
    'Black' o valores RGB en hexadecimal.
    """
    background: str = "black"
    foreground: str = "magenta"
    header_color: str = "green"
    separator_color: str = "white"
    key_color: str = "cyan"
    value_color: str = "white"
    time_bar_color: str = "cyan"
    volume_bar_color: str = "green"
    empty_bar_color: str = "#232323"

@dataclass
class UIConfig:
    """
    Configuraciones de UI, contiene a las configuraciones de portada, separador,
    barras y colores, ademas de toggles para los bordes y para desactivar los colores.
    """
    cover: CoverConfig = field(default_factory=CoverConfig)
    draw_borders: bool = True
    separator: SeparatorConfig = field(default_factory=SeparatorConfig)
    bars: BarsConfig = field(default_factory=BarsConfig)
    no_colors: bool = False
    colors: ColorsConfig = field(default_factory=ColorsConfig)

@dataclass
class AppConfig:
    """
    Configuraciones de aplicacion
    por ahora solo contiene el nombre de nuestro reproductor preferido
    puede ser cualquier string que este contenido en el nombre de bus del misno
    """
    favorite_player: str = "spotify"

@dataclass
class Config:
    """
    Todas la configuraciones
    """
    app: AppConfig = field(default_factory=AppConfig)
    ui: UIConfig = field(default_factory=UIConfig)

@dataclass
class ColorPairList:
    """
    Tabla de colores incializados en curses
    """
    background: int
    error: int
    alert: int
    table: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        for key, value in self.table.items():
            setattr(self, key, value)
