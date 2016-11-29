__author__ = 'brendan'

import os
import beesh
import TeamClass


data_dir = os.getcwd()
data_file_name = 'results.csv'
data = beesh.csv_to_list(data_dir, data_file_name, 1, 0)

schedule_file_name = 'schedule.csv'
schedule_data = beesh.csv_to_list(data_dir, schedule_file_name, 1, 1)
schedule = {}
for i in range(1, len(schedule_data)):
    for j in range(1, len(schedule_data[0])):
        team_name = schedule_data[0][j]
        week = i
        if schedule_data[i][j] != '':
            try:
                schedule[team_name][week] = schedule_data[i][j]
            except KeyError:
                schedule[team_name] = {week: schedule_data[i][j]}


dict_of_teams = {}

high_score = 0
low_score = 1000
for row in data:
    team_name = row[0]
    data_type = row[1]
    points = {}
    for j in range(len(row[2:])):
        try:
            points[j+1] = float(row[j+2])
        except:
            continue

    if team_name in dict_of_teams:
        team = dict_of_teams[team_name]
    else:
        team = TeamClass.Team(team_name)
        dict_of_teams[team_name] = team

    if data_type == 'performance':
        team.performance = points
    else:
        team.projection = points

    if min(team.performance.values()) < low_score:
        low_score = min(team.performance.values())
    if max(team.performance.values()) > high_score:
        high_score = max(team.performance.values())

    team.schedule = schedule[team_name]


luck_table = []
for team in dict_of_teams.values():
    team.wins, team.losses, team.record = team.calc_record(dict_of_teams)
    team.exp_wins = team.calc_exp_record(dict_of_teams)
    team.stddev = team.calc_stddev()
    team.luck = team.wins - team.exp_wins
    luck_table.append([team.name, team.wins, team.exp_wins, team.luck])
