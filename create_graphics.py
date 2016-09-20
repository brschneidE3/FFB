__author__ = 'brsch'

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

for team in dict_of_teams.values():
    team.wins, team.losses = team.calc_record(dict_of_teams)
    team.stddev = team.calc_stddev()


Xs = []
Ys = []
names = []

# Performance vs Projection
beesh.plt.figure(1)
for team_name in dict_of_teams.keys():
    team = dict_of_teams[team_name]
    Xs.append(sum(team.projection.values())/len(team.projection.values()))
    Ys.append(sum(team.performance.values())/len(team.performance.values()))
    beesh.plt.scatter(Xs[-1], Ys[-1])
    beesh.plt.annotate(' %s' % team.name, xy=(Xs[-1], Ys[-1]), size=15)

beesh.plt.plot(Xs, Xs, label='Indicates a team whose performance and projections are the same')
beesh.plt.legend(loc='lower right')
beesh.plt.ylabel('Average Performance', size=20)
beesh.plt.xlabel('Average Projection', size=20)
beesh.plt.title('Performance vs. Projection by Team', size=40)

weeks = range(1, max(team.performance.keys())+1)
list_of_performances = []
weekly_avg = {i: sum(team.performance[i] for team in dict_of_teams.values())/14. for i in weeks}
for team_name in dict_of_teams.keys():
    team = dict_of_teams[team_name]
    list_of_performances.append([team.performance[week] for week in weeks])

# Team performances on average
beesh.plt.figure(2)
ax = beesh.ClusteredBar([week - .5 for week in weeks], list_of_performances, 111, list_of_labels=dict_of_teams.keys())
beesh.plt.xlim(0.467, max(weeks) + .4645)
beesh.plt.xticks(weeks, size=20)
beesh.plt.yticks(size=20)
avgs = []
for week in weeks:
    avgs.append(weekly_avg[week])
    avgs.append(weekly_avg[week])
ax.plot([week - 1 + 0.4645 for week in weeks] + [week + .4645 for week in weeks],
        avgs, 'k--', label='Average')
ax.legend(loc='lower right')
beesh.plt.xlabel('Week', size=30)
beesh.plt.ylabel('Points', size=30)

# Individual team performances
fig = beesh.plt.figure(3)
subplot_no = 0
for team_name in dict_of_teams:
    team = dict_of_teams[team_name]
    subplot_no += 1
    fig.add_subplot(4, 4, subplot_no)
    beesh.plt.plot(weeks, [team.performance[week] for week in weeks], 'xk-')
    beesh.plt.ylim(low_score - 10, high_score + 10)
    beesh.plt.xlim(0, max(weeks) + 1)
    beesh.plt.xticks(weeks)
    beesh.plt.title(team_name)

# Variance by team
beesh.plt.figure(4)
stdevs = []
Xs = []
for team_name in dict_of_teams.keys():
    team = dict_of_teams[team_name]
    Xs.append(sum(team.performance.values())/len(team.performance.values()))
    stdevs.append(team.stddev)
    beesh.plt.scatter(Xs[-1], stdevs[-1])
    beesh.plt.annotate(' %s' % team.name, xy=(Xs[-1], stdevs[-1]), size=15)
beesh.plt.xlabel('Average Performance', size=20)
beesh.plt.ylabel('Standard Deviation', size=20)
beesh.plt.title('Performance vs. Variance by Team', size=40)

beesh.plt.show()
