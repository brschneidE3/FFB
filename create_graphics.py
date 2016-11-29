__author__ = 'brsch'

import os
import beesh
import TeamClass
from operator import itemgetter
import itertools

from load_data import dict_of_teams, low_score, high_score, luck_table


Xs = []
Ys = []
names = []
weeks = range(1, max(dict_of_teams[dict_of_teams.keys()[0]].performance.keys())+1)
week_num = len(weeks)

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
# beesh.plt.savefig(r'Graphics\perf_v_proj_%s.png' % week_num, bbox_inches='tight')


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
# ax.plot([week - 1 + 0.4645 for week in weeks] + [week + .4645 for week in weeks],
#         avgs, 'k--', label='Average')
week_xs = []
for week in weeks:
    week_xs.append(week - .5)
    week_xs.append(week + .5)
ax.plot(week_xs, avgs, 'k--', label='Average')
ax.legend(loc='lower left')
beesh.plt.xlabel('Week', size=30)
beesh.plt.ylabel('Points', size=30)
# beesh.plt.savefig(r'Graphics\league_perf_%s' % week_num)

# Individual team performances
fig = beesh.plt.figure(3)
subplot_no = 0
for team_name in dict_of_teams:
    team = dict_of_teams[team_name]
    subplot_no += 1
    fig.add_subplot(4, 4, subplot_no)
    markers = []
    for week in weeks:
        if team.record[week-1] == 1:
            markers.append('og-')
        else:
            markers.append('or-')
    markers = itertools.cycle(markers)
    for week in weeks:
        beesh.plt.plot(week, team.performance[week], markers.next(), linestyle='-', markersize=15)
    beesh.plt.plot(weeks, [team.performance[week] for week in weeks], 'k-')

    beesh.plt.ylim(low_score - 10, high_score + 10)
    beesh.plt.xlim(0, max(weeks) + 1)
    beesh.plt.xticks(weeks)
    beesh.plt.title(team_name)
# beesh.plt.savefig(r'Graphics\team_perf_%s' % week_num)

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
beesh.plt.ylabel('<--- More Consistent   Less Consistent --->', size=20)
beesh.plt.title('Performance vs. Variance by Team', size=40)
# beesh.plt.savefig(r'Graphics\var_by_team_%s' % week_num)

strength_of_schedule_table = []
for team in dict_of_teams.values():
    opp_wins = 0
    opp_losses = 0
    opp_points = 0
    for week in range(1, week_num+1):
        week_opp_name = team.schedule[week]
        week_opp = dict_of_teams[week_opp_name]
        opp_wins += week_opp.wins
        opp_losses += week_opp.losses
        opp_points += sum(week_opp.performance.values())
    team.prev_opponent_wins = opp_wins
    team.prev_opponent_losses = opp_losses
    team.prev_opponent_winpct = float(opp_wins)/float(opp_wins + opp_losses)
    team.prev_opponent_points = opp_points/(week_num**2)

    opp_wins = 0
    opp_losses = 0
    opp_points = 0
    for week in range(week_num+1, 14):
        week_opp_name = team.schedule[week]
        week_opp = dict_of_teams[week_opp_name]
        opp_wins += week_opp.wins
        opp_losses += week_opp.losses
        opp_points += sum(week_opp.performance.values())
    team.remaining_opponent_wins = opp_wins
    team.remaining_opponent_losses = opp_losses
    team.remaining_opponent_winpct = float(opp_wins)/float(opp_wins + opp_losses)
    team.remaining_opponent_points = opp_points/((13.-week_num)*week_num)

    strength_of_schedule_table.append([team.name,
                                       team.prev_opponent_winpct, team.prev_opponent_points,
                                       team.remaining_opponent_winpct, team.remaining_opponent_points])

# sort strength of schedule table by remaining opponent points
sorted_sos_table = sorted(strength_of_schedule_table, key=itemgetter(4), reverse=True)
beesh.PrintTabularResults(['Team', 'Previous Opponent Win %', 'Previous Opponent Avg Points',
                           'Remaining Opponent Win %', 'Remaining Opponent Avg Points'],
                          sorted_sos_table)

sorted_luck = sorted(luck_table, key=itemgetter(3), reverse=True)
Xs = [i for i in range(len(sorted_luck))]
Ys = [row[3] for row in sorted_luck]
fig, ax = beesh.plt.subplots()
luck = ax.bar(Xs, Ys)
for i in range(len(sorted_luck)):
    row = sorted_luck[i]
    beesh.plt.annotate(' %s' % row[0], xy=(i+.25, row[3]), size=20, rotation=90)
beesh.plt.title('Wins - Expected Wins', size=20)
beesh.plt.ylabel('Luck', size=20)

print '\n'
beesh.PrintTabularResults(['Team', 'Wins', 'Exp(Wins)', 'Luck'], sorted_luck)

beesh.plt.show()
