import chat
import text
import random

quotes_list = []

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