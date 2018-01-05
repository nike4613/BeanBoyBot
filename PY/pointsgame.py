import text
import players

def register(bot):
    bot.register_private_command("join", cmd_joingame)
    bot.register_public_command("join", cmd_joingame)
    
def cmd_joingame(bot, user, cmd, args, mode):
    """% gives the user 100 points and adds them to the system, if they are not already.
    [{%}]"""
    if bot.player_handler.player_is_playing(user):
        bot.send_whisper(user, text.msg_join_already_joined)
        return
    bot.send_whisper(user, text.msg_join_joining)
    bot.send_message(text.msg_join_welcome(player=user))
    bot.player_handler.player_join(user)
    
