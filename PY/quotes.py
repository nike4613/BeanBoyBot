import chat
import text
import random

quotes_list = []

def register_commands(bot):
    def cmd_addq(bot, user, cmd, args, mode):
        add_quote(' '.join(args))
        bot.send_whisper(user, text.msg_quote_added)
    def cmd_getq(bot, user, cmd, args, mode):
        id = -1
        try:
            id = int(args[0])
        except:
            pass
        qt = get_quote(id)
        bot.send_whisper(user, text.msg_quote_sent)
        bot.send_message(qt)

    bot.register_private_command("addquote", cmd_addq)
    bot.register_private_command("quote", cmd_getq)

def add_quote(quote):
    quotes_list.append(quote)
    
def get_quote(id):
    if id == -1 or id > len(quotes_list):
        id = random.random(1,len(quotes_list))
    return quotes_list[id-1]

def del_quote(id):
    if id == -1 or id > len(quotes_list):
        return
    del quotes_list[id-1]
    
def save(file):
    with open(file, 'w') as f:
        f.writelines(quotes_list)
        
def load(file):
    with open(file, 'r') as f:
        quotes_list = f.readlines()