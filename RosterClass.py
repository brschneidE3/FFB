__author__ = 'brendan'

import beesh

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

    weeks = {1: 1,  # Includes weightings for each week
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
             16: 1}

    def __init__(self):

        self.players = []

    def add_player(self, player):
        """
        Add a player to self.players and update self.positions
        """
        self.players.append(player)
        self.weekly_performance = self.calc_weekly_performance(players=self.players)

    def weekly_points(self, players):
        """
        weekly_points = {'QB': {1:  [p1 points, p2 points, ..., pN points], ...
                                17: [p1 points, p2 points, ..., pN points]},
                         ...
                         'D': {1:  [p1 points, p2 points, ..., pN points], ...
                                17: [p1 points, p2 points, ..., pN points]}
                        }
        """
        weekly_points = {pos: {week: [] for week in self.weeks.keys()} for pos in self.starting_pos}
        for player in players:
            for week in self.weeks.keys():
                weekly_points[player.pos][week].append(player.points[week]*self.weeks[week])

        for pos in weekly_points.keys():
            for week in self.weeks.keys():
                weekly_points[pos][week] = sorted(weekly_points[pos][week], reverse=True)

        return weekly_points

    def calc_weekly_performance(self, players):
        """
        weekly_performance = {'QB': {1:  w1_points, ..., 17: w17_points}, ..
                               'D': {1:  w1_points, ..., 17: w17_points}.
                              }
        """
        weekly_points = self.weekly_points(players)
        weekly_performance = {}
        for pos in self.starting_pos.keys():
            weekly_performance[pos] = {}
            # num_pos_on_roster = len(weekly_points[pos][1])
            num_starters = self.starting_pos[pos]
            for week in self.weeks.keys():
                weekly_performance[pos][week] = sum(weekly_points[pos][week][:num_starters])
        return weekly_performance

    def get_team_projection(self, players):
        """
        Returns season points projection
        """
        weekly_performance = self.calc_weekly_performance(players)
        team_projection = sum([sum(weekly_performance[pos].values()) for pos in weekly_performance.keys()])
        return team_projection

    def show_weekly_performance(self, weekly_performance):
        table = []
        for pos in ['QB', 'RB', 'WR', 'TE', 'K', 'DEF', 'D', 'DB']:
            new_row = [pos]
            for i in self.weeks.keys():
                new_row.append(weekly_performance[pos][i])
            new_row.append(sum(new_row[1:]))
            table.append(new_row)
        beesh.PrintTabularResults([''] + ['week%s' % i for i in self.weeks.keys()] + ['total'], table)