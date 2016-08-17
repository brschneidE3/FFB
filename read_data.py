__author__ = 'brendan'

import os
import beesh
import PlayerClass
import RosterClass

data_dir = os.getcwd()


def read():

    available_players = {}

    for pos in ['QB', 'RB']:
        pos_file = '%s.csv' % pos
        available_players[pos] = {}
        data_list = beesh.csv_to_list(data_dir, pos_file, 1, 0)

        for row in data_list:
            name, team_pos_string = row[0].rsplit('\xa0')
            team, pos = team_pos_string.rsplit(' - ')
            player = PlayerClass.Player(name, team, pos, row[1:])

            available_players[pos][player] = player.total
    return available_players
