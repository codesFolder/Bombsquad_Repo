import babase
import bauiv1 as bui
import bauiv1lib.party
import random
import bascenev1 as bs
from bascenev1 import screenmessage as push

# Word banks for GG messages
gg_words = [
    "Good Game!",
    "GG!",
    "Well played!",
    "Respect!",
    "Nice match!",
    "That was fun!",
    "GG, everyone!",
    "Well fought!"
]

# Some fun colors (R, G, B)
colors = [
    (1, 0, 0),     # Red
    (0, 1, 0),     # Green
    (0, 0, 1),     # Blue
    (1, 1, 0),     # Yellow
    (1, 0.5, 0),   # Orange
    (0.6, 0.2, 1)  # Purple
]

class GGPartyWindow(bauiv1lib.party.PartyWindow):
    def __init__(s, *args, **kwargs):
        super().__init__(*args, **kwargs)
        s._delay = s._a = 50  # cooldown (5 seconds)
        s._btn = bui.buttonwidget(
            parent=s._root_widget,
            size=(60, 40),
            scale=0.8,
            label='GG',
            button_type='square',
            position=(s._width - 70, s._height - 83),
            on_activate_call=s._send_gg
        )

    def _ok(s, a):
        if s._btn.exists():
            bui.buttonwidget(
                edit=s._btn,
                label=str((s._delay - a) / 10) if a != s._delay else 'GG'
            )
            s._a = a

    def _send_gg(s):
        if s._a != s._delay:
            push("Too fast!")
            return
        else:
            # Pick a random GG message and color
            msg = random.choice(gg_words)
            col = random.choice(colors)

            # Send the message with color
            bs.chatmessage(msg, color=col)

            # Play a sound effect
            bs.play_sound(bs.getsound('ding'))

            # Start cooldown
            for i in range(10, s._delay + 1):
                bs.apptimer((i - 10) / 10, bs.Call(s._ok, i))

# ba_meta require api 9

# ba_meta export babase.Plugin
class GGPlugin(babase.Plugin):
    def __init__(s):
        bauiv1lib.party.PartyWindow = GGPartyWindow
