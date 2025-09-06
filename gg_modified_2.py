# ba_meta require api 9
import babase
import bauiv1 as bui
import bauiv1lib.party
import random
import bascenev1 as bs
from bascenev1 import screenmessage as push

# --- Message Lists ---
# (Unchanged)
sorry_msgs = [
    "😅 Oops, my bad there!", "🙏 Sorry about that, didn’t mean to!",
    "🙇 My apologies, that was clumsy of me!", "😬 Whoops! Totally my fault.",
    "🙏 Sorry! I’ll make it up to you.", "😓 Didn’t mean to mess that up, sorry!",
    "🙁 My mistake, won’t happen again!", "🙇‍♂️ Apologies! That was on me."
]
gg_msgs = [
    "👏 Good game, everyone! That was fun. 🎉", "🏆 GG! Well played all around. 👏",
    "🤝 Wooo — that was a solid match! 💪", "🎯 Nice game! You all played great. 🙌",
    "🏅 GG! Let’s do that again sometime. 😄", "⚔️ Well fought, team! 💥",
    "🔥 GG! That was intense. 💯", "🎮 Good game! Thanks for playing. 😊"
]
taunt_msgs = [
    "😏 Is that your best shot...", "😂 I’ve seen toddlers throw harder than that!",
    "🐌 That move was so slow...", "⚠️ Careful, you might hurt yourself!",
    "🏆 If missing was a sport, you’d be champ.", "🙃 I almost felt that… almost.",
    "💨 You call that an attack?", "🎯 I’ve fought tougher opponents in the tutorial."
]


class PartyWindowWithButtons(bauiv1lib.party.PartyWindow):
    def __init__(s, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --- CUSTOMIZATION VARIABLES ---
        button_size = (50, 35)
        button_scale = 0.7
        start_pos_x = s._width - 60
        start_pos_y = s._height - 83
        horizontal_offset = 60
        vertical_offset = 0
        # --- END OF CUSTOMIZATION ---

        s._cooldown_seconds = 5.0

        # We've added a 'color' entry for each button.
        # Colors are (Red, Green, Blue) tuples, with values from 0.0 to 1.0.
        s._buttons_data = {
            'sorry': {
                'label': 'Sorry',
                'messages': sorry_msgs,
                'color': (1.0, 0.8, 0.3),  # Yellow
                'position': (start_pos_x, start_pos_y),
                'last_use_time': 0.0,
                'widget': None
            },
            'gg': {
                'label': 'GG',
                'messages': gg_msgs,
                'color': (0.4, 1.0, 0.4),  # Green
                'position': (start_pos_x - horizontal_offset,
                             start_pos_y - vertical_offset),
                'last_use_time': 0.0,
                'widget': None
            },
            'taunt': {
                'label': 'Taunt',
                'messages': taunt_msgs,
                'color': (1.0, 0.5, 0.3),  # Orange
                'position': (start_pos_x - (2 * horizontal_offset),
                             start_pos_y - (2 * vertical_offset)),
                'last_use_time': 0.0,
                'widget': None
            }
        }

        # The loop now also reads the 'color' data.
        for name, data in s._buttons_data.items():
            data['widget'] = bui.buttonwidget(
                parent=s._root_widget,
                size=button_size,
                scale=button_scale,
                label=data['label'],
                color=data['color'],  # <-- THE NEW LINE
                button_type='square',
                position=data['position'],
                on_activate_call=babase.Call(s._send_message, name)
            )

    def _send_message(s, name: str):
        button_data = s._buttons_data[name]
        now = babase.apptime()
        
        time_since_last_use = now - button_data['last_use_time']
        if time_since_last_use < s._cooldown_seconds:
            push("Too fast!")
            bui.getsound('error').play()
            return

        bs.chatmessage(random.choice(button_data['messages']))
        bui.getsound('swish').play()
        button_data['last_use_time'] = now

        s._update_cooldown_visual(name)

    def _update_cooldown_visual(s, name: str):
        button_data = s._buttons_data[name]

        if not button_data['widget'].exists():
            return
            
        now = babase.apptime()
        time_since_last_use = now - button_data['last_use_time']
        time_left = s._cooldown_seconds - time_since_last_use

        if time_left > 0:
            bui.buttonwidget(edit=button_data['widget'],
                             label=f'{time_left:.1f}')
            babase.apptimer(0.1, babase.Call(s._update_cooldown_visual, name))
        else:
            bui.buttonwidget(edit=button_data['widget'],
                             label=button_data['label'])

# ba_meta export babase.Plugin
class byBordd(babase.Plugin):
    def __init__(s):
        bauiv1lib.party.PartyWindow = PartyWindowWithButtons
