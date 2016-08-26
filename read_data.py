__author__ = 'brendan'

import os
import beesh
import PlayerClass
import DraftClass

data_dir = os.getcwd()


def read():

    available_players = {pos: {} for pos in DraftClass.list_of_positions}

    for pos in DraftClass.list_of_positions:

        if pos == 'DB':
            pass

        elif pos != 'D':
            pos_file = '%s.csv' % pos
            data_list = beesh.csv_to_list(data_dir, pos_file, 1, 0)

            for row in data_list:
                name, team_pos_string = row[0].rsplit('\xa0')
                team, pos_string = team_pos_string.rsplit(' - ')

                position = pos_string
                player = PlayerClass.Player(name, team, position, row[1:18], row[18])

                available_players[position][player] = player.total

        else:
            pos_file = '%s.csv' % pos
            data_list = beesh.csv_to_list(data_dir, pos_file, 1, 0)

            for row in data_list:
                try:
                    name, team_pos_string = row[0].rsplit('\xa0')
                    team, pos_string = team_pos_string.rsplit(' - ')

                    position = 'D'
                    player = PlayerClass.Player(name, team, position, row[1:18])
                    available_players[position][player] = player.total

                    if 'S' in pos_string or 'CB' in pos_string:
                        new_position = 'DB'
                        new_player = PlayerClass.Player(name, team, new_position, row[1:18])
                        available_players['DB'][new_player] = new_player.total
                except ValueError:
                    print row
                    print pos_file
                    exit()

    return available_players
