# texts
global_with = "with"
global_without = "without"

msg_splitgamedesc = "Now you can play a game in chat with the speedrun! "
					+ "The run will always have a 'cost' associated with it, "
					+ "and you can buy or sell the run at that price at any "
					+ "time. Think of it like a stock. Use '{pre}join' to add yourself "
					+ "into the game, '{pre}buy' to buy a run, '{pre}sell' to sell a run and "
					+ "'{pre}points' to see your points. A PB will give double points, "
					+ "but a reset will only give you 75% of the current cost. I'm still an early version, so "
					+ "sorry if something doesn't work. {pre}help for all commands."

msg_unknown_command = "Unknown command '{cmd}'. Please whisper '{priv_pre}help' for a list of commands."
msg_private_command = "The command '{cmd}' is whisper-only. Use '{pub_pre}talktome' to easily get a whisper chat window open."
msg_public_command = "The command '{cmd}' is main-chat only. Please see the '{priv_pre}help' command."

msg_help = "Chat commands: {public} ; Whisper commands: {privat}"

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