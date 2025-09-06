# ba_meta require api 9
import babase
import bascenev1 as bs
from babase import Plugin as v
from bauiv1 import buttonwidget as z, gettexture as x
from bauiv1lib.ingamemenu import InGameMenuWindow as InGameMenu
from bauiv1lib.mainmenu import MainMenuWindow as MainMenu
import bauiv1 as bui

# ====== CONFIGURABLE CONSTANTS ======

# Reconnect button in pause menu
REJOIN_SIZE = (23, 26)         # width, height
REJOIN_OFFSET_X = 60           # distance from right edge
REJOIN_OFFSET_Y = 60           # distance from top edge
REJOIN_COLOR = (0, 1, 0)       # green

# Favourite buttons in pause menu
PAUSE_FAV_START_X = 40         # starting X position
PAUSE_FAV_Y = 80               # vertical position from bottom
PAUSE_FAV_SIZE = (150, 40)     # width, height
PAUSE_FAV_GAP_X = 160          # horizontal gap between buttons
PAUSE_FAV_COLOR = (0.2, 0.6, 1)

# Favourite buttons in main menu
MAIN_FAV_START_X = 100
MAIN_FAV_Y = 70
MAIN_FAV_SIZE = (150, 40)
MAIN_FAV_GAP_X = 160
MAIN_FAV_COLOR = (0.2, 0.6, 1)

# Max favourites to keep
MAX_FAVS = 5

# ====================================

# ====== FAVOURITES LIST (auto-updated) ======
favourites = []
# ============================================

# Store last joined server
InGameMenu.i = InGameMenu.p = 0
_original_connect = bs.connect_to_party


def save_favourite(name, ip, port):
    global favourites
    new_entry = {"name": name, "ip": ip, "port": port}
    if new_entry not in favourites:
        favourites.append(new_entry)
        favourites = favourites[-MAX_FAVS:]


def reconnect(address, port=43210, print_progress=False):
    try:
        if bool(bs.get_connection_to_host_info_2()):
            bs.disconnect_from_host()
    except Exception:
        pass
    InGameMenu.i = address
    InGameMenu.p = port
    _original_connect(InGameMenu.i, InGameMenu.p, print_progress)
    babase.apptimer(1, check_and_save)


def check_and_save():
    info = bs.get_connection_to_host_info()
    if info and info.get('name'):
        save_favourite(info['name'], InGameMenu.i, InGameMenu.p)
    else:
        babase.apptimer(1, check_and_save)


# Add reconnect + favourites to in-game pause menu
def hook_ingame(func):
    def wrapper(self, *args, **kwargs):
        # Reconnect button (anchored top-right)
        z(
            parent=self._root_widget,
            size=REJOIN_SIZE,
            icon=x('replayIcon'),
            color=REJOIN_COLOR,
            on_activate_call=bs.Call(reconnect, InGameMenu.i, InGameMenu.p),
            position=(self._width - REJOIN_OFFSET_X, self._height - REJOIN_OFFSET_Y)
        )

        # Favourites list in pause menu
        start_x = PAUSE_FAV_START_X
        y = PAUSE_FAV_Y
        for fav in favourites:
            z(
                parent=self._root_widget,
                size=PAUSE_FAV_SIZE,
                label=fav["name"][:18],
                color=PAUSE_FAV_COLOR,
                on_activate_call=bs.Call(bs.connect_to_party, fav["ip"], fav["port"]),
                position=(start_x, y)
            )
            start_x += PAUSE_FAV_GAP_X

        return func(self, *args, **kwargs)
    return wrapper


# Draw favourites in main menu home screen
def hook_mainmenu(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        root = self._root_widget
        start_x = MAIN_FAV_START_X
        y = MAIN_FAV_Y
        for fav in favourites:
            z(
                parent=root,
                size=MAIN_FAV_SIZE,
                label=fav["name"][:18],
                color=MAIN_FAV_COLOR,
                on_activate_call=bs.Call(bs.connect_to_party, fav["ip"], fav["port"]),
                position=(start_x, y)
            )
            start_x += MAIN_FAV_GAP_X
        return result
    return wrapper


# ba_meta export babase.Plugin
class byBordd(v):
    def __init__(self):
        InGameMenu._refresh_in_game = hook_ingame(InGameMenu._refresh_in_game)
        MainMenu._refresh = hook_mainmenu(MainMenu._refresh)
        bs.connect_to_party = reconnect
