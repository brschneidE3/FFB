__author__ = 'brendan'

import operator

class Eval:

    def __init__(self, available_players, roster):
        self.available_players = available_players
        self.roster = roster

    def points_above_replacement(self, player_under_consideration, replaceable_players):

        max_par = -100000000
        for replaceable_player in replaceable_players:
            par = 0
            for week in range(1, 18):
                par += player_under_consideration.points[week] - replaceable_player.points[week]
            if par > max_par:
                max_par = par

        return max_par

    def rank_points_above_replacement(self, available_players, replaceable_players):

        par = {}

        for player in available_players:
            par[player] = self.points_above_replacement(player, replaceable_players)

        sorted_par = sorted(par.items(), key=operator.itemgetter(1), reverse=True)

        rank = 0
        for tup in sorted_par[:10]:
            rank += 1
            print "%s: %s, %s" % (rank, tup[0], tup[1])