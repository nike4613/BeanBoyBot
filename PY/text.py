# texts
global_with = "with"
global_without = "without"

msg_splitgamedesc = "Now you can play a game in chat with the speedrun! "\
                    + "The run will always have a 'cost' associated with it, "\
                    + "and you can buy or sell the run at that price at any "\
                    + "time. Think of it like a stock. Use '{pre}join' to add yourself "\
                    + "into the game, '{pre}buy' to buy a run, '{pre}sell' to sell a run and "\
                    + "'{pre}points' to see your points. A PB will give double points, "\
                    + "but a reset will only give you 75% of the current cost. I'm still an early version, so "\
                    + "sorry if something doesn't work. {pre}help for all commands."

msg_low_points = "{player}, looks like "\
                +   "you're low on points beanssMS . Luckily you "\
                +   "get 3 points for every minute watching, so "\
                +   "you'll be back in it in no time!"
                
msg_gambled_to_top_teir = "{player} MADE IT TO RANK {rank}! Keepo even if it was from gambling..."
msg_gamble_win = "HEY! You won {points} points! PogChamp"
msg_gamble_loose = "FeelsBadMan Too bad... you lost {points} points from that..."
msg_gamble_loose_bad = "HEY GUYS! {player} lost {points} points from GAMBLING! Thats why you shouldn't gamble."
msg_gamble_cant_gamble_words = "Hey now. You can't go gambling words."

msg_not_enough_points = "You don't have enough points to {action}."
msg_not_playing = "You have to be playing to do that."
                    
msg_unknown_command = "Unknown command '{cmd}'. Please whisper '{priv_pre}help' for a list of commands."
msg_private_command = "The command '{cmd}' is whisper-only. Use '{pub_pre}talktome' to easily get a whisper chat window open."
msg_public_command = "The command '{cmd}' is main-chat only. Please see the '{priv_pre}help' command."

msg_help = "Chat commands: {public} | Whisper commands: {privat}"
msg_help_please_use_whisper = "Please use whispers for as many future actions as you can to keep chat clean."

msg_join_already_joined = "You are already in the game!"
msg_join_joining = "Welcome to The Game! You start with 100 points. Don't waste them!"
msg_join_welcome = "Please welcome {player}, a brand new player in The Game!"

help_public_command = "{cmd} is a chat command."
help_private_command = "{cmd} is a whisper command."
help_command = "usage: {usage} | {doc}"

msg_talktome = "Hi, {name}! From now on, please talk to me in this window to keep the main chat clear. If you want to know what I can do, go ahead and use the 'help' command."

dbg_bot_connecting = "Connecting to Twitch IRC on port {port} as '{nick}' {wov6} IPv6 and {wossl} SSL."
dbg_cap_acknowledged = "CAP {cap} registered"
err_cap_nak = "ERROR: CAP {cap} not granted"
err_cap_denied = "ERROR: CAP {cap} denied"


# This mess makes it so you can do var_name(formatting, info) to format.
# It removes itself when done.
def _run():
    import sys
    class _t(str):
        def __call__(self, *args, **kwargs):
            return _t(self.format(*args, **kwargs))
    self = sys.modules[__name__]
    for k in vars(self):
        if type(vars(self)[k]) is str:
            vars(self)[k] = _t(vars(self)[k])
    vars(self)['_run'] = None
_run()