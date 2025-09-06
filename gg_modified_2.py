# ba_meta require api 9
import babase
import bauiv1 as bui
import bauiv1lib.party
import random
import bascenev1 as bs
from bascenev1 import screenmessage as push

# --- Message Lists ---
# (These are unchanged)
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

        # The cooldown time in seconds for all buttons.
        s._cooldown_seconds = 5.0

        # This dictionary is the core of our new design.
        # It holds all the info for each button in one place.
        # To add a new button, you just add a new entry here.
        s._buttons_data = {
            'sorry': {
                'label': 'Sorry',
                'messages': sorry_msgs,
                'position': (start_pos_x, start_pos_y),
                'last_use_time': 0.0,  # We now track time instead of a counter.
                'widget': None         # A placeholder for the button widget itself.
            },
            'gg': {
                'label': 'GG',
                'messages': gg_msgs,
                'position': (start_pos_x - horizontal_offset,
                             start_pos_y - vertical_offset),
                'last_use_time': 0.0,
                'widget': None
            },
            'taunt': {
                'label': 'Taunt',
                'messages': taunt_msgs,
                'position': (start_pos_x - (2 * horizontal_offset),
                             start_pos_y - (2 * vertical_offset)),
                'last_use_time': 0.0,
                'widget': None
            }
        }

        # This loop creates all the buttons automatically.
        for name, data in s._buttons_data.items():
            data['widget'] = bui.buttonwidget(
                parent=s._root_widget,
                size=button_size,
                scale=button_scale,
                label=data['label'],
                button_type='square',
                position=data['position'],
                # This lambda function is key. It tells the button to call
                # our one single function, passing its own name ('sorry', etc.)
                on_activate_call=babase.Call(s._send_message, name)
            )

    def _send_message(s, name: str):
        """A single, reusable function to handle clicks for ALL buttons."""
        button_data = s._buttons_data[name]
        now = babase.apptime() # Get the current game time.
        
        # Check the cooldown.
        time_since_last_use = now - button_data['last_use_time']
        if time_since_last_use < s._cooldown_seconds:
            push("Too fast!")
            bui.getsound('error').play()
            return

        # If cooldown is over, send a message and update the time.
        bs.chatmessage(random.choice(button_data['messages']))
        bui.getsound('swish').play()
        button_data['last_use_time'] = now

        # Start the visual cooldown timer.
        s._update_cooldown_visual(name)

    def _update_cooldown_visual(s, name: str):
        """A single, reusable function to update the button's label."""
        button_data = s._buttons_data[name]

        # Safety check: if the button/window is gone, just stop.
        if not button_data['widget'].exists():
            return
            
        now = babase.apptime()
        time_since_last_use = now - button_data['last_use_time']
        time_left = s._cooldown_seconds - time_since_last_use

        if time_left > 0:
            # If still on cooldown, show the remaining time.
            bui.buttonwidget(edit=button_data['widget'],
                             label=f'{time_left:.1f}')
            # Schedule this function to run again in 0.1 seconds to continue the countdown.
            babase.apptimer(0.1, babase.Call(s._update_cooldown_visual, name))
        else:
            # Cooldown is over, restore the original label.
            bui.buttonwidget(edit=button_data['widget'],
                             label=button_data['label'])

# ba_meta export babase.Plugin
class byBordd(babase.Plugin):
    def __init__(s):
        bauiv1lib.party.PartyWindow = PartyWindowWithButtons
