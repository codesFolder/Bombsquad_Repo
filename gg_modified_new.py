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
    "😅 Oops, my bad there!",
    "🙏 Sorry about that, didn’t mean to!",
    "🙇 My apologies, that was clumsy of me!",
    "😬 Whoops! Totally my fault.",
    "🤦 Yikes… that one’s on me.",
    "🙃 Well… that didn’t go as planned.",
    "😔 Sorry team, I’ll make it up to you!",
    "🥴 My bad, I was half asleep there.",
    "💢 Ugh, I messed that up big time.",
]

gg_msgs = [
    "👏 Good game, everyone! That was fun. 🎉",
    "🏆 GG! Well played all around. 👏",
    "🤝 Wooo — that was a solid match! 💪",
    "🎯 Nice game! You all played great. 🙌",
    "🔥 GGWP! That was intense.",
    "💯 Respect — you guys brought your A-game.",
    "🎮 That’s how you play! GG.",
    "🥳 Fun match! Let’s do it again sometime.",
    "⚡ GG! That ending was wild.",
]

taunt_msgs = [
    "😏 Is that your best shot?",
    "😂 I’ve seen toddlers throw harder than that!",
    "🐌 That move was so slow, I had time to make a sandwich. 🥪",
    "⚠️ Careful, you might hurt yourself swinging like that!",
    "🪶 That attack tickled.",
    "📦 Return to sender — weak delivery.",
    "🥱 Wake me up when you actually land a hit.",
    "🎯 You’re aiming… somewhere, I guess?",
    "🧊 Cold moves… and not in a good way.",
]

greet_msgs = [
    "Hey everyone! 👋",
    "Hello! Ready for a game? 😄",
    "Hi there! GLHF!",
    "Yo! Let's do this. 🔥",
    "👑 The champ has arrived!",
    "🎮 Who’s ready to lose? 😉",
    "🚀 Let’s blast off into this match!",
    "🍀 Good luck, you’ll need it.",
    "⚡ Let’s make this quick and fun.",
]

bye_msgs = [
    "GG, gotta go. Bye! 👋",
    "That's all for me, see ya!",
    "Fun games! Catch you all later.",
    "I'm out, take care everyone!",
    "💨 Vanishing like a ninja — bye!",
    "🎯 That’s my last round, peace out.",
    "🍻 Good games, I’m off!",
    "🛑 Logging off before I get too good.",
    "🌙 Night all, GG!",
]

react_msgs = [
    "bruh",
    "wtf",
    "lol",
    "damn!",
    "oof",
    "💀",
    "🔥",
    "😭",
    "😱",
    "EZ",
    "sheeeesh",
    "🤯",
]


class PartyWindowWithButtons(bauiv1lib.party.PartyWindow):
    def __init__(s, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --- CUSTOMIZATION VARIABLES ---
        button_size = (50, 35)
        button_scale = 0.7
        start_pos_x = s._width - 30
        start_pos_y = s._height - 83
        horizontal_offset = 0
        vertical_offset = 40
        s._cooldown_seconds = 5.0
        # --- END OF CUSTOMIZATION ---

        # NEW: Added a 'shuffled_queue' to each button's data.
        # This will hold our "shuffled deck" of messages.
        s._buttons_data = {
            'sorry': {
                'label': 'Sorry',
                'messages': sorry_msgs,
                'color': (1.0, 0.8, 0.3),  # Yellow
                'shuffled_queue': [],      # <-- Starts empty
                'position': (start_pos_x, start_pos_y),
                'last_use_time': 0.0,
                'widget': None
            },
            'gg': {
                'label': 'GG',
                'messages': gg_msgs,
                'color': (0.4, 1.0, 0.4),  # Green
                'shuffled_queue': [],      # <-- Starts empty
                'position': (start_pos_x - horizontal_offset,
                             start_pos_y - vertical_offset),
                'last_use_time': 0.0,
                'widget': None
            },
            'taunt': {
                'label': 'Taunt',
                'messages': taunt_msgs,
                'color': (0.6, 0.4, 0.8),   # Lavender
                'shuffled_queue': [],      # <-- Starts empty
                'position': (start_pos_x - (2 * horizontal_offset),
                             start_pos_y - (2 * vertical_offset)),
                'last_use_time': 0.0,
                'widget': None
            },
            'greet': {
                'label': 'greet',
                'messages': greet_msgs,
                'color': (1.0, 0.5, 0.3),  # Orange
                'shuffled_queue': [],      # <-- Starts empty
                'position': (start_pos_x - (3 * horizontal_offset),
                             start_pos_y - (3 * vertical_offset)),
                'last_use_time': 0.0,
                'widget': None
            },
            'bye': {
                'label': 'bye',
                'messages': bye_msgs,
                'color': (1.0, 0.75, 0.8),  # Pink
                'shuffled_queue': [],      # <-- Starts empty
                'position': (start_pos_x - (4 * horizontal_offset),
                             start_pos_y - (4 * vertical_offset)),
                'last_use_time': 0.0,
                'widget': None
            },
            'react': {
                'label': 'react',
                'messages': react_msgs,
                'color': (0.1, 0.1, 0.4),   # Navy Blue
                'shuffled_queue': [],      # <-- Starts empty
                'position': (start_pos_x - (5 * horizontal_offset),
                             start_pos_y - (5 * vertical_offset)),
                'last_use_time': 0.0,
                'widget': None
            },
        }

        for name, data in s._buttons_data.items():
            data['widget'] = bui.buttonwidget(
                parent=s._root_widget,
                size=button_size,
                scale=button_scale,
                label=data['label'],
                color=data['color'],
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

        # --- THE NEW LOGIC IS HERE ---
        
        # 1. Check if our shuffled queue is empty.
        if not button_data['shuffled_queue']:
            # If it is, create a fresh, shuffled copy of the original messages.
            new_queue = button_data['messages'].copy()
            random.shuffle(new_queue)
            button_data['shuffled_queue'] = new_queue
            # print(f"Refilled '{name}' queue.") # Optional: for debugging

        # 2. Pop one message from the end of our shuffled queue.
        message_to_send = button_data['shuffled_queue'].pop()
        
        # 3. Send the unique message.
        bs.chatmessage(message_to_send)
        
        # --- END OF NEW LOGIC ---

        bui.getsound('swish').play()
        button_data['last_use_time'] = now
        s._update_cooldown_visual(name)

    def _update_cooldown_visual(s, name: str):
        # (This function is unchanged)
        button_data = s._buttons_data[name]
        if not button_data['widget'].exists(): return
        now = babase.apptime()
        time_left = (button_data['last_use_time'] + s._cooldown_seconds) - now
        if time_left > 0:
            bui.buttonwidget(edit=button_data['widget'], label=f'{time_left:.1f}')
            babase.apptimer(0.1, babase.Call(s._update_cooldown_visual, name))
        else:
            bui.buttonwidget(edit=button_data['widget'], label=button_data['label'])

# ba_meta export babase.Plugin
class byBordd(babase.Plugin):
    def __init__(s):
        bauiv1lib.party.PartyWindow = PartyWindowWithButtons
