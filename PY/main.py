import irc.client
import argparse
import socket

import chat
import text
import livesplit
import quotes

emr_player_info = '._player_info_emr'
emr_quotes = '._quotes_emr'

def arg_parse():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-c','--channel', default='BeanSSBM', type=str.lower,
        help='the Twitch channel to connect to')
    parser.add_argument('--no-ssl', action='store_false', dest='use_ssl',
        help='disables the use of SSL when connecting to twitch')
    parser.add_argument('-6', '--use-v6', action='store_true',
        help='enables the use of IPv6 to connect to Twitch')
    parser.add_argument('-k','--key', default='',
        help="the OAuth key to use to connect to Twitch")
    parser.add_argument('-n','--nick', default='testBot',
        help="username of account being logged into")
    parser.add_argument('-s', '--server-port', default=8080, type=int,
        help='the port to use for the HTTP server')
    parser.add_argument('-o', '--split-host', default='localhost', type=str,
        help='the host for the split server')
    parser.add_argument('-p', '--split-port', default=16384, type=int,
        help='the port to use to connect to the split server')
    
    return parser.parse_args()

def main():
    args = arg_parse()
    
    bot = chat.TwitchChatBot(args.channel, args.key, args.nick, args.use_ssl, args.use_v6)
    
    bot.reactor.add_global_handler("all_events", print, 0) # this prints all events
    
    import os.path
    if os.path.isfile(emr_player_info):
        print(text.dbg_load_emr_playerinfo)
        bot.player_handler.load_from_file(emr_player_info)
    if os.path.isfile(emr_quotes):
        print(text.dbg_load_emr_quotes)
        quotes.load(emr_quotes)
    
    bot.split_conn_def = (args.split_host, args.split_port)
    bot.split_conn = None
    bot.split_client = None
    try:
        print(text.dbg_connecting_split(host=bot.split_conn_def[0],port=bot.split_conn_def[1]))
        bot.split_conn = socket.create_connection(bot.split_conn_def, 5)
        bot.split_client = livesplit.LiveSplitClient(bot.split_conn)
        print(text.dbg_split_connected)
    except socket.timeout:
        eprint(text.dbg_split_timeout)
    except ConnectionRefusedError:
        eprint(text.dbg_split_refused)
        
    bot.connect()
    try:
        bot.start()
    except:
        bot.split_conn.close()
        bot.connection.close()
        bot.player_handler.save_to_file(emr_player_info)
        quotes.save(emr_quotes)
        raise
    
def eprint(*args, **kwargs):
    import sys
    print(*args, file=sys.stderr, **kwargs) 

if __name__ == "__main__":
    main()