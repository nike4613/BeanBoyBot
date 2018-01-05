from irc.client import SimpleIRCClient, NickMask
from irc.connection import Factory
import ssl
import main, quotes, text
import sys

CAP_MEMBERSHIP = 'twitch.tv/membership'
CAP_COMMANDS = 'twitch.tv/commands'

class TwitchChatBot(SimpleIRCClient):
    
    def __init__(self, channel, oauth, nick, usessl, usev6):
        super(TwitchChatBot, self).__init__()
    
        self.target_channel = "#"+channel
        self.oauth_key = oauth
        self.nick = nick
        self.use_ssl = usessl
        self.use_v6 = usev6
        
        self.pub_commands = {}
        self.pub_prefix = ';'
        self.priv_commands = {}
        self.priv_prefix = ''
        
        self.caps = []
        
        self.users = set()
        
        _register_commands(self)
        
    def connect(self):
        wrap = lambda x:x
        port = 6667
        if self.use_ssl:
            wrap = ssl.wrap_socket
            port = 443
        fac = Factory(wrapper=wrap,ipv6=self.use_v6)
        
        print(text.dbg_bot_connecting(
            port=port,
            nick=self.nick,
            wov6=(text.global_with if self.use_v6 else text.global_without),
            wossl=(text.global_with if self.use_ssl else text.global_without)
        ))
        
        super(TwitchChatBot, self).connect('irc.chat.twitch.tv', port, self.nick,
            connect_factory=fac, password='oauth:'+self.oauth_key)
        
    def get_caps(self):
        self.connection.cap('REQ',':' + CAP_MEMBERSHIP) # request Twitch's membership capability
        self.connection.cap('REQ', ':' + CAP_COMMANDS) # lets us send whispers
        
    def on_cap(self, conn, evt):
        if evt.arguments[0] == "ACK":
            print(text.dbg_cap_acknowledged(cap=evt.arguments[1]))
            self.caps.append(evt.arguments[1])
        if evt.arguments[0] == "NAK":
            eprint(text.err_cap_denied(cap=evt.arguments[1]))
        
    def on_welcome(self, conn, evt):
        conn.join(self.target_channel)
        self.get_caps()
    
    def on_whisper(self, conn, evt):
        """
        whisper sent (needs command cap)
        """
        nm = NickMask(evt.source)
        name = nm.nick
        message = ' '.join(evt.arguments)
        print("WHISPER:", message, "FROM:", name)
        if message.startswith(self.priv_prefix):    
            #self.send_whisper('daniske',' '.join(["PRIV_COMMAND:", message, "FROM:", name]))
            # process cmd
            argv = message.split(' ')
            argv[0] = argv[0][len(self.priv_prefix):]
            self.handle_commands(conn, name, argv, False)
            
    def on_pubmsg(self, conn, evt):
        """
        A message in the public chat.
        """
        nm = NickMask(evt.source)
        name = nm.nick
        if name not in self.users:
            self.users.add(name)
        message = ' '.join(evt.arguments)
        print("MESSAGE:", message, "FROM:", name)
        if message.startswith(self.pub_prefix): 
            #self.send_whisper('daniske',' '.join(["COMMAND:", message, "FROM:", name]))
            # process cmd
            argv = message.split(' ')
            argv[0] = argv[0][len(self.pub_prefix):]
            self.handle_commands(conn, name, argv, True)
    
    def handle_commands(self, conn, name, argv, ispub):
        if argv[0] in self.pub_commands:
            if ispub:
                self.pub_commands[argv[0]](self, name, argv[0], argv[1:], "public")
                return
            elif argv[0] not in self.priv_commands:
                self.send_whisper(name, text.msg_public_command(cmd=argv[0],priv_pre=self.priv_prefix))
                return
        if argv[0] in self.priv_commands:
            if ispub:
                self.send_message(text.msg_private_command(cmd=argv[0],pub_pre=self.pub_prefix))
            else:
                self.priv_commands[argv[0]](self, name, argv[0], argv[1:], "private")
            return
        if ispub:
            self.send_message(text.msg_unknown_command(cmd=argv[0],priv_pre=self.pub_prefix))
        else:
            self.send_whisper(name, text.msg_unknown_command(cmd=argv[0],priv_pre=self.priv_prefix))
        
    def on_join(self, conn, evt):
        nm = NickMask(evt.source)
        name = nm.nick
        self.users.add(name)
    def on_part(self, conn, evt):
        nm = NickMask(evt.source)
        name = nm.nick
        self.users.discard(name)
        
    def get_users(self):
        return frozenset(self.users)
        
    def set_public_prefix(self, pre):
        self.pub_prefix = pre
    def set_private_prefix(self, pre):
        self.priv_prefix = pre
    def register_public_command(self, name, handler):
        self.pub_commands[name] = handler
    def register_private_command(self, name, handler):
        self.priv_commands[name] = handler
        
    def send_message(self, message, target=None):
        if target is None:
            target = target = self.target_channel
        print("SEND '" + message.replace('\r','').replace('\n','') + "' TO " + target)
        self.connection.privmsg(target, message.replace('\r','').replace('\n',''))
    def send_whisper(self, target, message):
        if CAP_COMMANDS in self.caps:
            self.send_message('/w '+target+' '+message, '#jtv')
        else:
            eprint(text.err_cap_nak(cap=CAP_COMMANDS))

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    
def _register_commands(bot):
    def cmd_help(bot, user, cmd, args, mode):
        """% lists commands, and provides more info on them.
        [{% [command]}]"""
        #bot.send_whisper(user, "I am a Twitch bot written in Python to replace BeanSSBM's Java bot. I currently can do very little.")
        if len(args) == 0:
            publ = ', '.join([bot.pub_prefix + s for s in bot.pub_commands.keys()])
            priv = ', '.join([bot.priv_prefix + s for s in bot.priv_commands.keys()])
            bot.send_whisper(user, text.msg_help(public=publ, privat=priv) \
                + ((" | " + text.msg_help_please_use_whisper) if mode == "public" else ""))
        else:
            cmd = args[0]
            func = None
            ispub = None
            if cmd in bot.pub_commands:
                ispub = True
                func = bot.pub_commands[cmd]
            if cmd in bot.priv_commands:
                ispub = False
                func = bot.priv_commands[cmd]
            if func is None:
                bot.send_whisper(user, text.msg_unknown_command(cmd=cmd,priv_pre=bot.priv_prefix))
                return
            
            pre = bot.pub_prefix if ispub else bot.priv_prefix
            
            pp = (text.help_public_command if ispub else text.help_private_command)(cmd=pre+cmd)
            
            import re
            doc = func.__doc__
            doc = re.sub(r'(\A|([^\\]))%', r'\2'+pre+cmd, doc)
            doc = doc.replace(r'\%', '%')
            
            srch = re.search(r'\[{(.*)}\]', doc)
            doc = re.sub(r'\[{.*}\]', '', doc)
            doc = doc.strip()
            gr0 = pre+cmd
            if srch is not None:
                gr0 = srch.group(1)
            
            bot.send_whisper(user, text.help_command(usage=gr0,pubpriv=pp,doc=doc)\
                + ((" | " + text.msg_help_please_use_whisper) if mode == "public" else ""))     
    def cmd_talktome(bot, user, cmd, args, mode):
        """% whispers the user to make it easy to open.
        [{%}]"""
        bot.send_whisper(user, text.msg_talktome(name=user))
        
    bot.register_private_command("help", cmd_help)
    bot.register_public_command("help", cmd_help)
    bot.register_public_command("talktome", cmd_talktome)
    
    import commands
    commands.register(bot)