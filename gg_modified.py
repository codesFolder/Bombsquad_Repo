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

class PartyWindowWithTwoIndependentCooldowns(bauiv1lib.party.PartyWindow):
    def __init__(s, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Separate cooldowns
        s._delay_sorry = s._a_sorry = 50
        s._delay_gg = s._a_gg = 50

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

        # GG button (shifted left)
        s._btn_gg = bui.buttonwidget(
            parent=s._root_widget,
            size=(50, 35),
            scale=0.7,
            label='GG',
            button_type='square',
            position=(s._width - 120, s._height - 83),
            on_activate_call=s._send_gg
        )

    # Update Sorry button label
    def _ok_sorry(s, a):
        if s._btn_sorry.exists():
            bui.buttonwidget(edit=s._btn_sorry,
                             label=str((s._delay_sorry - a) / 10) if a != s._delay_sorry else 'Sorry')
            s._a_sorry = a

    # Update GG button label
    def _ok_gg(s, a):
        if s._btn_gg.exists():
            bui.buttonwidget(edit=s._btn_gg,
                             label=str((s._delay_gg - a) / 10) if a != s._delay_gg else 'GG')
            s._a_gg = a

    def _apologize(s):
        if s._a_sorry != s._delay_sorry:
            push("Too fast!")
            return
        bs.chatmessage(random.choice(lmao).replace('%', random.choice(sory)).replace('$', random.choice(cash)))
        for i in range(10, s._delay_sorry + 1):
            bs.apptimer((i - 10) / 10, bs.Call(s._ok_sorry, i))

    def _send_gg(s):
        if s._a_gg != s._delay_gg:
            push("Too fast!")
            return
        bs.chatmessage(random.choice(gg_msgs))
        for i in range(10, s._delay_gg + 1):
            bs.apptimer((i - 10) / 10, bs.Call(s._ok_gg, i))

# ba_meta export babase.Plugin
class byBordd(babase.Plugin):
    def __init__(s):
        bauiv1lib.party.PartyWindow = PartyWindowWithTwoIndependentCooldowns
