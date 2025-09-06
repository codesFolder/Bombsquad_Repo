# ba_meta require api 9
import babase
import bauiv1 as bui
import bauiv1lib.party
import random
import bascenev1 as bs
from bascenev1 import screenmessage as push

# Sorry messages
sorry_msgs = [
    "😅 Oops, my bad there!",
    "🙏 Sorry about that, didn’t mean to!",
    "🙇 My apologies, that was clumsy of me!",
    "😬 Whoops! Totally my fault.",
    "🙏 Sorry! I’ll make it up to you.",
    "😓 Didn’t mean to mess that up, sorry!",
    "🙁 My mistake, won’t happen again!",
    "🙇‍♂️ Apologies! That was on me."
]

# GG messages
gg_msgs = [
    "👏 Good game, everyone! That was fun. 🎉",
    "🏆 GG! Well played all around. 👏",
    "🤝 Wooo — that was a solid match! 💪",
    "🎯 Nice game! You all played great. 🙌",
    "🏅 GG! Let’s do that again sometime. 😄",
    "⚔️ Well fought, team! 💥",
    "🔥 GG! That was intense. 💯",
    "🎮 Good game! Thanks for playing. 😊"
]

# Taunt messages
taunt_msgs = [
    "😏 Is that your best shot, or are you just warming up for me?",
    "😂 I’ve seen toddlers throw harder than that!",
    "🐌 That move was so slow, I had time to make a sandwich. 🥪",
    "⚠️ Careful, you might hurt yourself swinging like that!",
    "🏆 If missing was a sport, you’d be the world champion. 😜",
    "🙃 I almost felt that… almost.",
    "💨 You call that an attack? I call it a gentle breeze.",
    "🎯 I’ve fought tougher opponents in the tutorial."
]

class PartyWindowWithThreeButtons(bauiv1lib.party.PartyWindow):
    def __init__(s, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Independent cooldowns
        s._delay_sorry = s._a_sorry = 50
        s._delay_gg = s._a_gg = 50
        s._delay_taunt = s._a_taunt = 50

        # Sorry button (rightmost)
        s._btn_sorry = bui.buttonwidget(
            parent=s._root_widget,
            size=(50, 35),
            scale=0.7,
            label='Sorry',
            button_type='square',
            position=(s._width - 60, s._height - 83),
            on_activate_call=s._send_sorry
        )

        # GG button (middle)
        s._btn_gg = bui.buttonwidget(
            parent=s._root_widget,
            size=(50, 35),
            scale=0.7,
            label='GG',
            button_type='square',
            position=(s._width - 120, s._height - 83),
            on_activate_call=s._send_gg
        )

        # Taunt button (leftmost)
        s._btn_taunt = bui.buttonwidget(
            parent=s._root_widget,
            size=(50, 35),
            scale=0.7,
            label='Taunt',
            button_type='square',
            position=(s._width - 180, s._height - 83),
            on_activate_call=s._send_taunt
        )

    # Update labels for cooldown
    def _ok_sorry(s, a):
        if s._btn_sorry.exists():
            bui.buttonwidget(edit=s._btn_sorry,
                             label=str((s._delay_sorry - a) / 10) if a != s._delay_sorry else 'Sorry')
            s._a_sorry = a

    def _ok_gg(s, a):
        if s._btn_gg.exists():
            bui.buttonwidget(edit=s._btn_gg,
                             label=str((s._delay_gg - a) / 10) if a != s._delay_gg else 'GG')
            s._a_gg = a

    def _ok_taunt(s, a):
        if s._btn_taunt.exists():
            bui.buttonwidget(edit=s._btn_taunt,
                             label=str((s._delay_taunt - a) / 10) if a != s._delay_taunt else 'Taunt')
            s._a_taunt = a

    # Button actions
    def _send_sorry(s):
        if s._a_sorry != s._delay_sorry:
            push("Too fast!")
            return
        bs.chatmessage(random.choice(sorry_msgs))
        for i in range(10, s._delay_sorry + 1):
            bs.apptimer((i - 10) / 10, bs.Call(s._ok_sorry, i))

    def _send_gg(s):
        if s._a_gg != s._delay_gg:
            push("Too fast!")
            return
        bs.chatmessage(random.choice(gg_msgs))
        for i in range(10, s._delay_gg + 1):
            bs.apptimer((i - 10) / 10, bs.Call(s._ok_gg, i))

    def _send_taunt(s):
        if s._a_taunt != s._delay_taunt:
            push("Too fast!")
            return
        bs.chatmessage(random.choice(taunt_msgs))
        for i in range(10, s._delay_taunt + 1):
            bs.apptimer((i - 10) / 10, bs.Call(s._ok_taunt, i))

# ba_meta export babase.Plugin
class byBordd(babase.Plugin):
    def __init__(s):
        bauiv1lib.party.PartyWindow = PartyWindowWithThreeButtons
