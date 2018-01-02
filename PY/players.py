# player manager
import text

class PlayerExistsError(Exception):
    pass
class PlayerDoesntExistError(Exception):
    pass

class PlayerState(object):
    def __init__(self, id):
        import uuid
        self.uuid = uuid.UUID(int=id)
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.uuid == other.uuid
        return False
PlayerState.NONE = PlayerState(0)
PlayerState.INVESTED = PlayerState(1)
PlayerState.SELL_WAITING = PlayerState(2)

import pickle
class PlayerHandler(object):
    def __init__(self, bot):
        self.players = {}
        self.player_order = []
        self.bot = bot
    def player_is_playing(self, player):
        return player in self.players.keys()
    def player_join(self, player):
        if self.player_is_playing(player):
            raise PlayerExistsError("Player " + player + "is already playing")
            
        ply = {name:player,points:100,state:PlayerState.NONE,invested:0,split:-1}
        self.players[player] = ply
    def save_to_file(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self.players, f)
    def save_to_java_format(self, file):
        with open(file, 'w') as f:
            lines = ["{}:{}:{}:{}".format(p.name,p.points,p.state.uuid.int,p.invested) for n,p in self.players.items()]
            f.writelines(lines)
    def load_from_file(self, file):
        with open(file, 'rb') as f:
            self.players = pickle.load(f)
        self.order_players()
    def load_from_java_format(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()
            lmb = lambda s: {name:s[0],points:int(s[1]),state:PlayerState(int(s[3])),invested:s[4],split:-1}
            plyl = [lmb(l.split(':')) for l in lines]
            for o in plyl:
                self.players[o.name] = o
        self.order_players()
    def set_begin_split(self, split):
        for k,p in self.players.items():
            if p.state == PlayerState.INVESTED:
                p.split = split
    def get_player_invested(self, player):
        return self.players[player].invested
    def set_player_invested(self, player, invest):
        self.players[player].invested = invest
    def give_all_invested(self, points):
        for k,p in self.players.items():
            if p.state == PlayerState.INVESTED:
                self.add_points(p.name,points)
    def get_investors(self):
        return sum([p.state != PlayerState.NONE for n,p in self.players.items()]) # True == 1
    def get_points(self, player):
        return self.players[player].points
    def add_points(self, player, amount): # a removal is just adding a negative value
        self.players[player].points += amount
        if self.players[player].points < 0:
            self.players[player].points = 0
        # handle limits
        # low is the only one set (@30)
        if self.players[player].points < 30:
            self.bot.send_whisper(player, text.msg_low_points(player=player))
    def set_player_state(self, player, state):
        self.players[player].state = state
    def get_player_state(self, player):
        return self.players[player].state
    def order_players(self):
        self.player_order = sorted(self.players.keys(),key=lambda s:self.players[s].points)[::-1]
    def get_player_placement(self, player): 
        self.order_players()
        
        try:
            return self.player_order.index(player)+1
        except ValueError:
            raise PlayerDoesntExistError("Player " + player + "is not playing" )
    def get_leaderboard(self):
        self.order_players()
        
        out = ""
        top = self.player_order[0:5]
        for i, p in enumerate(top):
            if out != "":
                out += " | "
            out += "#{}: {} with {}".format(i+1,p.name, p.points)
            
        return out
        