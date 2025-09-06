# ba_meta require api 9
import babase
import bauiv1 as bui
import bauiv1lib.party
import random
import bascenev1 as bs
from bascenev1 import screenmessage as push

# GG messages
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

# Colors (R, G, B)
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
        s._delay = 50  # cooldown ticks
        s._a = s._delay  # start ready
        s._btn = bui.buttonwidget(
            parent=s._root_widget,
            size=(60, 40),
            scale=0.8,
            label='GG',
            button_type='square',
            position=(s._width - 70, s._height - 83),
            on_activate_call=s._send_gg
        )
        print("[GGPlugin] GG Button created in PartyWindow")

    def _ok(s, a):
        if s._btn.exists():
            bui.buttonwidget(
                edit=s._btn,
                label=str((s._delay - a) / 10) if a != s._delay else 'GG'
            )
            s._a = a

    def _send_gg(s):
        print(f"[GGPlugin] Button clicked. Cooldown: {s._a}/{s._delay}")
        if s._a != s._delay:
            push("Too fast!")
            print("[GGPlugin] Click blocked by cooldown")
            return

        msg = random.choice(gg_words)
        col = random.choice(colors)

        try:
            # Send to chat if available
            bs.chatmessage(msg, color=col)
            # Always show on screen
            bs.screenmessage(msg, color=col)
            print(f"[GGPlugin] Sent message: '{msg}' with color {col}")
        except Exception as e:
            print(f"[GGPlugin] ERROR sending message: {e}")

        try:
            bs.play_sound(bs.getsound('ding'))
            print("[GGPlugin] Played sound: ding")
        except Exception as e:
            print(f"[GGPlugin] ERROR playing sound: {e}")

        # Start cooldown
        for i in range(10, s._delay + 1):
            bs.apptimer((i - 10) / 10, bs.Call(s._ok, i))

# ba_meta export babase.Plugin
class GGPlugin(babase.Plugin):
    def on_app_running(self):
        print("[GGPlugin] App running — overriding PartyWindow")
        bauiv1lib.party.PartyWindow = GGPartyWindow
