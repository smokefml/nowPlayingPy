import asyncio
from .player_bus_connection import PlayerBusConnection
from tools.cover_tools import no_cover, get_cover
from config.loader import get_config

class PlayingInfo:
    """
    Inicializa objetos convenientes para consumir en la UI
    """
    def __init__(self, meta, player, position, status, volume, repeat, shuffle, note=''):
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
        self.repeat = repeat
        self.shuffle = shuffle
        self.note = note

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
        self.repeat = None
        self.shuffle = False
        self.note = ''
        # Cover
        self._last_cover = ''
        self.cover = no_cover()
        self.should_refresh = False
        # Referencia reservada para la tarea de actualización
        self._update_task = None

    async def update_info(self):
        """
        Refresca el estado de reproduccion con la informacion en el bus
        Estas solicitudes fuerzan la coneccion con el reproducotor en el bus
        """
        self.metadata = await self.manager.get_metadata()
        self.player = await self.manager.get_identity()
        self.position = await self.manager.get_position()
        self.status = await self.manager.get_status()
        self.volume = await self.manager.get_volume()
        self.repeat = await self.manager.get_loop_status()
        self.shuffle = await self.manager.get_shuffle()
        self.note = ''
        self.update_cover()

        if self.player is None:
            self.set_note('No hay reproductores activos.')

    def update_cover(self):
        """
        Refresca el estado de la portada
        """
        self.cover = get_cover(self.metadata)
        # Nos aseguramos de que cover ES SIEMPRE un PATH
        if self.cover is None or not self.cover:
            self.cover = no_cover()
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
                           self.status, self.volume, self.repeat,
                           self.shuffle, self.note)

    def get_cover_path(self):
        """
        Devuelve el estado actual de la portada, URI local y si se tiene que
        refrescar en pantalla
        """
        return self.cover, self.should_refresh

    def set_note(self, note: ''):
        self.note = note

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

    async def clean(self):
        """
        Tareas de limpieza antes de salir
        Detiene la tarea de actualizacion y cierra la coneccion con el bus
        """
        self.stop_update_loop()
        await self.manager.disconnect()

    # --- Métodos de control del reproductor que usan el manager ---
    async def play_pause(self):
        try:
            await self.manager.play_pause()
            return self.status.lower()
        except Exception as e:
            emsg = f"{e}"
            if "not available" in emsg:
                self.set_note("Acción no disponible")
            else:
                self.set_note(emsg)
        return None

    async def next_track(self):
        try:
            await self.manager.next_track()
            return 'next_track'
        except Exception as e:
            emsg = f"{e}"
            if "not available" in emsg:
                self.set_note("Acción no disponible")
            else:
                self.set_note(emsg)
            return None

    async def previous_track(self):
        try:
            await self.manager.previous_track()
            return 'previous_track'
        except Exception as e:
            emsg = f"{e}"
            if "not available" in emsg:
                self.set_note("Acción no disponible")
            else:
                self.set_note(emsg)
            return None

    async def stop(self):
        try:
            await self.manager.stop()
            return 'stop'
        except Exception as e:
            emsg = f"{e}"
            if "not available" in emsg:
                self.set_note("Acción no disponible")
            else:
                self.set_note(emsg)
            return None

    async def seek_f5s(self):
        try:
            await self.manager.seek(5)
            return 'seek_f5s'
        except Exception as e:
            emsg = f"{e}"
            if "not available" in emsg:
                self.set_note("Acción no disponible")
            else:
                self.set_note(emsg)
            return None

    async def seek_b5s(self):
        try:
            await self.manager.seek(-5)
            return 'seek_b5s'
        except Exception as e:
            emsg = f"{e}"
            if "not available" in emsg:
                self.set_note("Acción no disponible")
            else:
                self.set_note(emsg)
            return None

    async def volume_up(self):
        if not self.volume:
            return None
        newvol = self.volume + 0.05
        newvol = min(newvol, 1.00)
        newvol = max(newvol, 0.00)
        try:
            if await self.manager.set_volume(newvol):
                self.volume = newvol
                return 'vol+'
            return None
        except Exception as e:
            self.set_note(f'{e}')
            return None

    async def volume_down(self):
        if not self.volume:
            return None
        newvol = self.volume - 0.05
        newvol = min(newvol, 1.00)
        newvol = max(newvol, 0.00)
        try:
            if await self.manager.set_volume(newvol):
                self.volume = newvol
                return 'vol-'
            return None
        except Exception as e:
            self.set_note(f'{e}')
            return None

PLAYBACK_CONTROL = None

async def get_control():
    global PLAYBACK_CONTROL
    if PLAYBACK_CONTROL is None:
        PLAYBACK_CONTROL = PlayBackControl()
        await PLAYBACK_CONTROL.async_init()
    return PLAYBACK_CONTROL
