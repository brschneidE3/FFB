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
        weekly_points = {pos: {week: [] for week in range(1, 18)} for pos in self.starting_pos}
        for player in players:
            for week in range(1, 18):
                weekly_points[player.pos][week].append(player.points[week])

        for pos in weekly_points.keys():
            for week in range(1, 18):
                weekly_points[pos][week] = sorted(weekly_points[pos][week], reverse=True)

        return weekly_points

    def calc_weekly_performance(self, players):
        """
        weekly_performance = {'QB': {1:  w1_points, ..., 17: w17_points}, ...
                               'D': {1:  w1_points, ..., 17: w17_points}
                              }
        """
        weekly_points = self.weekly_points(players)
        weekly_performance = {}
        for pos in self.starting_pos:
            weekly_performance[pos] = {}
            num_pos_on_roster = len(weekly_points[pos][1])
            pos_needed = self.starting_pos[pos]
            if num_pos_on_roster >= pos_needed:
                for week in range(1, 18):
                    weekly_performance[pos][week] = sum(weekly_points[pos][week][:num_pos_on_roster])
            else:
                for week in range(1, 18):
                    weekly_performance[pos][week] = 0
        return weekly_performance

    def get_team_projection(self):
        """
        Returns season points projection
        """
        team_projection = sum([sum(self.weekly_performance[pos].values()) for pos in self.weekly_performance.keys()])
        return team_projection

    @staticmethod
    def show_weekly_performance(weekly_performance):
        table = []
        for pos in ['QB', 'RB', 'WR', 'TE', 'K', 'DEF', 'D', 'DB']:
            new_row = [pos]
            for i in range(1, 18):
                new_row.append(weekly_performance[pos][i])
            new_row.append(sum(new_row[1:]))
            table.append(new_row)
        beesh.PrintTabularResults([''] + ['week%s' % i for i in range(1, 18)] + ['total'], table)