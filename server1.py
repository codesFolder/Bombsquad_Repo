# ba_meta require api 9
import bascenev1 as bs
from babase import Plugin as v
from bauiv1 import buttonwidget as z, gettexture as x
from bauiv1lib.ingamemenu import InGameMenuWindow as m

m.i = m.p = 0
_original_connect = bs.connect_to_party

def j(address, port=43210, print_progress=False):
    try:
        if bool(bs.get_connection_to_host_info_2()):
            bs.disconnect_from_host()
    except:
        pass
    m.i = address
    m.p = port
    # Send a quick chat message before reconnecting
    try:
        bs.chatmessage("🔄 Rejoining last server...")
    except:
        pass
    _original_connect(m.i, m.p, print_progress)

def R(s):
    def w(t, *f, **g):
        # Bigger, green button with tooltip
        z(
            parent=t._root_widget,
            size=(35, 35),  # bigger size
            color=(0, 1, 0),  # green
            icon=x('replayIcon'),
            tooltip="Reconnect to last server",
            on_activate_call=bs.Call(j, m.i, m.p)
        )
        return s(t, *f, **g)
    return w

# ba_meta export babase.Plugin
class byBordd(v):
    def __init__(s):
        m._refresh_in_game = R(m._refresh_in_game)
        bs.connect_to_party = j
