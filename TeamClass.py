__author__ = 'brsch'

import statistics

class Team:

    def __init__(self, name):

        self.name = name

        self.projection = None
        self.performance = None
        self.schedule = None
        self.wins = 0
        self.losses = 0

    def calc_record(self, dict_of_teams):
        wins = 0
        losses = 0

        for week in self.performance.keys():
            weekly_opponent = dict_of_teams[self.schedule[week]]
            opponent_score = weekly_opponent.performance[week]
            score = self.performance[week]

            if opponent_score > score:
                losses += 1
            else:
                wins += 1
        return wins, losses

    def calc_stddev(self):
        return statistics.stdev(self.performance.values())