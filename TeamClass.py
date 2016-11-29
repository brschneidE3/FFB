__author__ = 'brsch'

import statistics
import operator
from numpy.random import normal

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
        record = []

        for week in self.performance.keys():
            weekly_opponent = dict_of_teams[self.schedule[week]]
            opponent_score = weekly_opponent.performance[week]
            score = self.performance[week]

            if opponent_score > score:
                losses += 1
                record.append(0)
            else:
                wins += 1
                record.append(1)
        return wins, losses, record

    def calc_exp_record(self, dict_of_teams):
        exp_wins = 0.
        num_opps = len(dict_of_teams.keys()) - 1

        for week in self.performance.keys():
            score = self.performance[week]

            for opp in dict_of_teams.values():
                opp_score = opp.performance[week]
                if opp_score < score:
                    exp_wins += 1./num_opps
        return exp_wins

    def calc_stddev(self):
        return statistics.stdev(self.performance.values())

class League:

    def __init__(self, dict_of_teams):

        self.dict_of_teams = dict_of_teams
        self.teams = dict_of_teams.values()
        self.num_teams = len(self.teams)
        self.len_of_season = 13
        self.top_n_makeplayoffs = 6
        self.weeks_played = len(dict_of_teams.values()[0].performance.keys())

    def get_standings(self, teams=None, additional_wins=None, additional_points=None):

        if teams is None:
            teams = self.teams

        wins_partition = []
        wins_seen = {}
        for team in teams:

            if additional_points is None:
                add_points = 0
            else:
                add_points = additional_points[team.name]
            if additional_wins is None:
                add_wins = 0
            else:
                add_wins = additional_wins[team.name]

            wins = team.wins + add_wins

            if wins in wins_seen.keys():
                i = wins_seen[wins]
                wins_partition[i].append((team.name,
                                          wins,
                                          sum(team.performance.values()) + add_points,
                                          team))
            else:
                try:
                    i = max(wins_seen.values()) + 1
                    wins_seen[wins] = i
                    wins_partition.append([(team.name,
                                            wins,
                                            sum(team.performance.values()) + add_points,
                                            team)])
                except ValueError:
                    wins_seen[wins] = 0
                    wins_partition.append([(team.name,
                                            wins,
                                            sum(team.performance.values()) + add_points,
                                            team)])

        standings = {}
        i = 0
        for win_total in sorted(wins_seen.keys(), reverse=True):
            list_of_teams = wins_partition[wins_seen[win_total]]
            sorted_list_of_teams = sorted(list_of_teams, key=operator.itemgetter(2), reverse=True)
            for name, wins, points, team in sorted_list_of_teams:
                i += 1
                standings[i] = (name, wins, points)
        return standings

    def add_points_and_wins_forecast(self, teams=None):

        if teams is None:
            teams = self.teams

        additional_wins = {}
        additional_points = {}

        for team in teams:
            for week in range(self.weeks_played + 1, self.len_of_season + 1):
                avg_points = sum(team.performance.values())/self.weeks_played
                std_dev = team.stddev

                opponent_name = team.schedule[week]
                opponent = self.dict_of_teams[opponent_name]
                opponent_avg_points = sum(opponent.performance.values())/self.weeks_played
                opponent_std_dev = opponent.stddev

                exp_points = normal(avg_points, std_dev, 1)[0]
                opp_exp_points = normal(opponent_avg_points, opponent_std_dev, 1)[0]

                try:
                    additional_points[team.name] += exp_points
                except KeyError:
                    additional_points[team.name] = exp_points

                if exp_points > opp_exp_points:
                    win = 1
                else:
                    win = 0

                try:
                    additional_wins[team.name] += win
                except KeyError:
                    additional_wins[team.name] = win

        return additional_wins, additional_points