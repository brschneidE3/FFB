__author__ = 'brendan'

import beesh
import bisect

class Roster:

    starting_pos = {
        'QB': 1,
        'RB': 2,
        'WR': 3,
        'TE': 1,
        'K': 1,
        'DEF': 1,
        'D': 2,
        'DB': 1,
    }

    weeks = {1: 0,  # Includes weightings for each week
             2: 1,
             3: 1,
             4: 1,
             5: 1,
             6: 1,
             7: 1,
             8: 1,
             9: 1,
             10: 1,
             11: 1,
             12: 1,
             13: 1,
             14: 1,
             15: 1,
             16: 1,
             17: 0}

    def __init__(self, players=None):

        self.players = players if players is not None else []
        self.performance = self.get_projection()

    def calc_weekly_performance(self):

        # weekly_points = {'QB': {1:  [p1 points, p2 points, ..., pN points], ...
        #                         17: [p1 points, p2 points, ..., pN points]},
        #                  ...
        #                  'D': {1:  [p1 points, p2 points, ..., pN points], ...
        #                         17: [p1 points, p2 points, ..., pN points]}
        #                 }
        weekly_points = {pos: {week: [] for week in self.weeks.keys()} for pos in self.starting_pos}
        for player in self.players:
            for week in self.weeks.keys():
                weekly_points[player.position][week].append(player.points[week]*self.weeks[week])
        for position in weekly_points.keys():
            for week in self.weeks.keys():
                weekly_points[position][week] = sorted(weekly_points[position][week], reverse=True)

        weekly_performance = {}
        for position in self.starting_pos.keys():
            weekly_performance[position] = {}
            num_starters = self.starting_pos[position]
            for week in self.weeks.keys():
                weekly_performance[position][week] = sum(weekly_points[position][week][:num_starters])

        return weekly_performance

    def get_projection(self):

        weekly_performance = self.calc_weekly_performance()
        projection = sum([sum(weekly_performance[position].values()) for position in weekly_performance.keys()])
        return projection

    def show_weekly_performance(self):
        weekly_performance = self.calc_weekly_performance()
        table = []
        for pos in ['QB', 'RB', 'WR', 'TE', 'K', 'DEF', 'D', 'DB']:
            new_row = [pos]
            for i in self.weeks.keys():
                new_row.append(weekly_performance[pos][i])
            new_row.append(sum(new_row[1:]))
            table.append(new_row)
        beesh.PrintTabularResults([''] + ['week%s' % i for i in self.weeks.keys()] + ['total'], table)