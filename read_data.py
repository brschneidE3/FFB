__author__ = 'brendan'

import os
import beesh
import PlayerClass
import RosterClass

data_dir = os.getcwd()


def read():

    list_of_qbs = []

    for pos_file in ['QB.csv']:
        data_list = beesh.csv_to_list(data_dir, pos_file, 1, 0)

        for row in data_list:
            name, team_pos_string = row[0].rsplit('\xa0')
            team, pos = team_pos_string.rsplit(' - ')
            player = PlayerClass.Player(name, team, pos, row[1:])
            list_of_qbs.append(player)

    return list_of_qbs

loqbs = read()
<<<<<<< HEAD
roster = RosterClass.Roster()
roster.add_player(loqbs[0])
weekly_performance = roster.calc_weekly_performance(roster.players)
roster.show_weekly_performance(weekly_performance)
print "team projection: %s" % roster.get_team_projection()
=======

eval_instance = EvalClass.Eval(available_players=loqbs[1:],
                               roster=[loqbs[0]]
                               )
eval_instance.rank_points_above_replacement(available_players=eval_instance.available_players,
                                            replaceable_players=eval_instance.roster
                                            )
print eval_instance.roster[0]
>>>>>>> 1ceb9368d2e993f4dd8bad6e3c1f94cece4299d9
