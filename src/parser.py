import json
import re


def get_killed(sentence):
    killed_regex = re.compile(r'killed (.*) by')
    mo = killed_regex.search(sentence)
    return mo.group(1)


def get_killer(sentence):
    killer_regex = re.compile(r'\d: (.*) killed')
    mo = killer_regex.search(sentence)
    return mo.group(1)


def get_player_info(sentence):
    player_regex = re.compile(r'n\\(.*)\\t\\')
    mo = player_regex.search(sentence)
    return mo.group(1)


def get_id_player(sentence):
    id_player_regex = re.compile(r': \d n\\')
    mo = id_player_regex.search(sentence)
    return int(mo.group()[2])


games = []
players = []
actually_game = {}
status = {}
game = 1
total_kills = 0
with open('..\log\Quake.txt', 'r') as f:
    for line_content in f.readlines():
        if 'Kill' in line_content:
            total_kills += 1
            killer = get_killer(line_content)
            killed = get_killed(line_content)

            for player in players:
                if player['nome'] == killed and killer == '<world>':
                    player['kills'] -= 1
                if player['nome'] == killer:
                    player['kills'] += 1

        if 'ClientUserinfoChanged' in line_content:
            name = get_player_info(line_content)
            id_player = get_id_player(line_content) - 1
            not_found = True
            for player in players:
                if player['id'] == id_player:
                    if player['nome'] != name:
                        old_name = player['nome']
                        player['old_names'].append(old_name)
                        player['nome'] = name
                    not_found = False
                    break
            if not_found:
                players.append({"id": id_player, "nome": name, "kills": 0, "old_names": []})
                id_player += 1

        if 'ShutdownGame' in line_content:
            status = {"total_kills": total_kills, "players": players}
            games.append({'game': game, 'status': status})
            status = {}
            game += 1
            total_kills = 0
            id_player = 1
            players = []

with open('Parser.json', 'w') as f:
    f.write(json.dumps(games))
input('Arquivo Parser criado com sucesso!')
