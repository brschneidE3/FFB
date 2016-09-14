__author__ = 'brendan'

import beesh
import PlayerClass
import os

data_dir = os.getcwd()
datafiles = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF', 'D']


def read():

    all_players = []
    players_by_pos = {'QB': {},
                         'RB': {},
                         'WR': {},
                         'TE': {},
                         'K': {},
                         'DEF': {},
                         'D': {},
                         'DB': {}}

    for datafile in datafiles:
        csv_name = '%s.csv' % datafile
        csv_data = beesh.csv_to_list(data_dir, csv_name, 1, 0)

        for row in csv_data:
            # print row
            name, team_pos_string = row[0].rsplit('\xa0')
            team, pos_string = team_pos_string.rsplit(' - ')

            if datafile == 'D':
                if 'CB' in pos_string or 'S' in pos_string:
                    position = 'DB'
                else:
                    position = 'D'
            else:
                position = pos_string

            player = PlayerClass.Player(name, team, position, row[1:18], row[18])
            dict_value = '%s - %s' % (player.name, player.team)
            all_players.append(player)

            players_by_pos[position][player] = dict_value

    return all_players, players_by_pos
