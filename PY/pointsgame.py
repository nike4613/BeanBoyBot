import text
import players
import timer

def register(bot):
    bot.register_private_command("join", cmd_joingame)
    bot.register_public_command("join", cmd_joingame)
    
    bot.register_private_command("points", cmd_view_points)
    
    init_point_timer(bot)
    
def cmd_joingame(bot, user, cmd, args, mode):
    """% gives the user 100 points and adds them to the system, if they are not already.
    [{%}]"""
    if bot.player_handler.player_is_playing(user):
        bot.send_whisper(user, text.msg_join_already_joined)
        return
    bot.send_whisper(user, text.msg_join_joining)
    bot.send_message(text.msg_join_welcome(player=user))
    bot.player_handler.player_join(user)
    
def cmd_view_points(bot, user, cmd, args, mode):
    """% shows the user's points to them.
    [{%}]"""
    if not bot.player_handler.player_is_playing(user):
        bot.send_whisper(user, text.msg_not_playing)
        return
    bot.send_whisper(user, text.msg_get_points(points=bot.player_handler.get_points(user)))
    
timers = []

def init_point_timer(bot):
    def point_adder():
        viewers = bot.get_users()
        for v in viewers:
            if bot.player_handler.player_is_playing(v):
                bot.player_handler.add_points(v, 1)
    time = timer.Timer(20, point_adder)
    timers.append(time)
    time.start()