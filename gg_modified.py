# ba_meta require api 9
import babase
import bauiv1 as bui
import bauiv1lib.party
import random
import bascenev1 as bs
from bascenev1 import screenmessage as push

# "%" random from sory
# "$" random from cash
sory = ["Sorry", "Sry", "Sryyy", "Sorryy"]
cash = ["My bad", "My fault", "My mistake", "My apologize"]
lmao = [
    "Oops %",
    "% didn't mean to",
    "%, that happens",
    "$, apologies!",
    "Ah I slipped, very %",
    "$, didn't mean to.",
    "Ah, % about that",
    "A- I did that $",
    "%, didn't mean to.",
    "$, forgive the slip",
    "%, didn't mean to mess up",
    "Ah % $",
    "$, forgive the error",
    "%, $ entirely"
]

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

class PartyWindowWithTwoButtons(bauiv1lib.party.PartyWindow):
    def __init__(s, *args, **kwargs):
        super().__init__(*args, **kwargs)
        s._delay = s._a = 50  # cooldown shared for both buttons

        # Sorry button (original position)
        s._btn_sorry = bui.buttonwidget(
            parent=s._root_widget,
            size=(50, 35),
            scale=0.7,
            label='Sorry',
            button_type='square',
            position=(s._width - 60, s._height - 83),
            on_activate_call=s._apologize
        )

        # GG button (shifted left by ~60px)
        s._btn_gg = bui.buttonwidget(
            parent=s._root_widget,
            size=(50, 35),
            scale=0.7,
            label='GG',
            button_type='square',
            position=(s._width - 120, s._height - 83),
            on_activate_call=s._send_gg
        )

    def _ok(s, a):
        if s._btn_sorry.exists():
            bui.buttonwidget(edit=s._btn_sorry,
                             label=str((s._delay - a) / 10) if a != s._delay else 'Sorry')
        if s._btn_gg.exists():
            bui.buttonwidget(edit=s._btn_gg,
                             label=str((s._delay - a) / 10) if a != s._delay else 'GG')
        s._a = a

    def _apologize(s):
        if s._a != s._delay:
            push("Too fast!")
            return
        bs.chatmessage(random.choice(lmao).replace('%', random.choice(sory)).replace('$', random.choice(cash)))
        for i in range(10, s._delay + 1):
            bs.apptimer((i - 10) / 10, bs.Call(s._ok, i))

    def _send_gg(s):
        if s._a != s._delay:
            push("Too fast!")
            return
        bs.chatmessage(random.choice(gg_msgs))
        for i in range(10, s._delay + 1):
            bs.apptimer((i - 10) / 10, bs.Call(s._ok, i))

# ba_meta export babase.Plugin
class byBordd(babase.Plugin):
    def __init__(s):
        bauiv1lib.party.PartyWindow = PartyWindowWithTwoButtons
