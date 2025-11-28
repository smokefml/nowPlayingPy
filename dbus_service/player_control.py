import asyncio
from .player_bus_connection import PlayerBusConnection
from tools.cover_tools import no_cover, get_cover
from config.loader import get_config

class PlayingInfo:
    """
    Inicializa objetos convenientes para consumir en la UI
    """
    def __init__(self, meta, player, position, status, volume):
        self.player = player
        self.title = meta.get("xesam:title", "STOP")
        self.artists = meta.get("xesam:artist", [])
        self.artist = ', '.join(self.artists)
        self.album = meta.get("xesam:album", '')
        self.length_us = meta.get("mpris:length", 0)
        self.length = self.length_us / 1000000 if self.length_us else 0
        self.position_us = position
        self.position = self.position_us / 1000000
        self.status = status
        self.volume = volume
        self.note = ''

        if self.player is None:
            self.note = "No hay reproductores activos."

class PlayBackControl:
    """
    Clase para controlar la coneccion con un reproductor en el bus
    desde un lugar central
    """
    def __init__(self):
        # Objeto de Conexion con Bus
        self.manager = PlayerBusConnection(get_config().app.favorite_player)
        # Info
        self.metadata = {}
        self.player = ''
        self.position = 0
        self.status = ''
        self.volume = None
        # Cover
        self._last_cover = ''
        self.cover = no_cover()
        self.should_refresh = False
        # Poblamos los atributos la primera vez al crear el objeto
        self._update_task = None

    async def update_info(self):
        """
        Refresca el estado de reproduccion con la informacion en el bus
        """
        self.metadata = await self.manager.get_metadata()
        self.player = await self.manager.get_identity()
        self.position = await self.manager.get_position()
        self.status = await self.manager.get_status()
        self.volume = await self.manager.get_volume()
        self.update_cover()

    def update_cover(self):
        """
        Refresca el estado de la portada
        """
        self.cover = get_cover(self.metadata)
        if self.cover != self._last_cover:
            self.should_refresh = True
            self._last_cover = self.cover

    def set_cover_should_refresh(self):
        """
        Pone el flag para mandar a refrescar la portada
        """
        self.should_refresh = True

    def set_cover_refreshed(self):
        """
        Limpia el flag, informando que se ha refrescado la portada en pantalla
        """
        self.should_refresh = False

    def get_info(self):
        """
        Devuelve un objeto con el estado actual de la informacion de reproduccion
        """
        return PlayingInfo(self.metadata, self.player, self.position,
                           self.status, self.volume)

    def get_cover_path(self):
        """
        Devuelve el estado actual de la portada, URI local y si se tiene que
        refrescar en pantalla
        """
        return self.cover, self.should_refresh

    # --- Gestion del bucle de actualizacion ---
    async def _update_loop(self):
        """
        Bucle infinito para actualizar la informacion periodicamente.
        """
        while True:
            await self.update_info()
            # Espera 1 segundo antes de la proxima actualizacion
            await asyncio.sleep(1)

    async def async_init(self):
        """Realiza la primera actualización y comienza el bucle."""
        # Esperamos aquí a que se obtenga la info por primera vez
        await self.update_info() 
        # Luego iniciamos el bucle periódico
        self.start_update_loop()

    def start_update_loop(self):
        """
        Inicia la tarea asincrona en segundo plano.
        """
        if self._update_task is None or self._update_task.done():
            # Creamos una tarea de asyncio que se ejecuta concurrentemente
            self._update_task = asyncio.create_task(self._update_loop())

    def stop_update_loop(self):
        """
        Cancela la tarea de actualizacion.
        """
        if self._update_task and not self._update_task.done():
            self._update_task.cancel()
            self._update_task = None
    
    # --- Opcional: Métodos de control del reproductor que usan el manager ---
    async def play_pause(self):
        await self.manager.play_pause()
    
    async def next_track(self):
        await self.manager.next_track()

    async def previous_track(self):
        await self.manager.previous_track()

PLAYBACK_CONTROL = None

async def get_control():
    global PLAYBACK_CONTROL
    if PLAYBACK_CONTROL is None:
        PLAYBACK_CONTROL = PlayBackControl()
        await PLAYBACK_CONTROL.async_init()
    return PLAYBACK_CONTROL
