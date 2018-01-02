import quotes
import players
import text
import pointsgame

def register(bot):
    bot.player_handler = players.PlayerHandler(bot)
    
    bot.register_private_command("gamble", cmd_gamble)
    pointsgame.register(bot)
    
def cmd_gamble(bot, user, cmd, args, mode):
    """Gamble your life savings away with this ONE SIMPLE TRICK! may cause a mild case of death Kappa
    [{% amount}]"""
    if not bot.player_handler.player_is_playing(user):
        bot.send_whisper(user, text.msg_not_playing)
        return
    
    togamble = 0
    try:
        togamble = abs(int(args[0]))
    except Exception:
        bot.send_whisper(user, text.msg_gamble_cant_gamble_words)
        
    if togamble > bot.player_handler.get_points(user):
        bot.send_whisper(user, text.msg_not_enough_points(action="gamble " + togamble + " points"))
        return
        
    from random import random
    
    # randomizing chance... MUAHAHAHA
    chance = random()
    win = random() <= chance
    
    oldplace = bot.player_handler.get_player_placement(user)
    
    if win:
        bot.player_handler.add_points(user, togamble)
        bot.send_whisper(user, text.msg_gamble_win(points=togamble))
        
        newplace = bot.player_handler.get_player_placement(user)
        if newplace > oldplace and newplace <= 5:
            bot.send_message(text.msg_gambled_to_top_teir(player=user,rank=newplace))
    else:
        bot.player_handler.add_points(user, -togamble)
        bot.send_whisper(user, text.msg_gamble_loose(points=togamble))
        
        if togamble >= 500:
            bot.send_message(text.msg_gamble_loose_bad(player=user,points=togamble))