# ba_meta require api 9
import babase
import bauiv1 as bui
import bauiv1lib.party
import random
import bascenev1 as bs
from bascenev1 import screenmessage as push

# GG messages
gg_msgs = [
    "Good Game!",
    "GG!",
    "Well played!",
    "Respect!",
    "Nice match!",
    "That was fun!",
    "GG, everyone!",
    "Well fought!"
]

class SorryPW(bauiv1lib.party.PartyWindow):
    def __init__(s, *args, **kwargs):
        super().__init__(*args, **kwargs)
        s._delay = s._a = 50  # 5 seconds
        s._btn = bui.buttonwidget(
            parent=s._root_widget,
            size=(50, 35),
            scale=0.7,
            label='GG',
            button_type='square',
            position=(s._width - 60, s._height - 83),
            on_activate_call=s._apologize
        )

    def _ok(s, a):
        if s._btn.exists():
            bui.buttonwidget(
                edit=s._btn,
                label=str((s._delay - a) / 10) if a != s._delay else 'GG'
            )
            s._a = a
        else:
            return

    def _apologize(s):
        if s._a != s._delay:
            push("Too fast!")
            return
        else:
            bs.chatmessage(random.choice(gg_msgs))
            for i in range(10, s._delay + 1):
                bs.apptimer((i - 10) / 10, bs.Call(s._ok, i))

# ba_meta export babase.Plugin
class byBordd(babase.Plugin):
    def __init__(s):
        bauiv1lib.party.PartyWindow = SorryPW
