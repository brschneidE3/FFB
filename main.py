# import create_graphics
from load_data import dict_of_teams
import TeamClass
import beesh
import operator

league = TeamClass.League(dict_of_teams)
league.get_standings()

total_rankings = {team: {rank: 0 for rank in range(1, 15)} for team in league.dict_of_teams.keys()}

N = 10000
n = 0
for draw in range(N):
    add_wins, add_points = league.add_points_and_wins_forecast()
    forecasted_standings = league.get_standings(additional_wins=add_wins, additional_points=add_points)

    for i in range(1, 15):
        name, wins, points = forecasted_standings[i]
        total_rankings[name][i] += 1

    n += 1
    if n % 1000 == 0:
        print '%s simulations complete' % n

table = []
for team in total_rankings.keys():
    new_row = [team.replace(' ', '_')]
    avg_rank = 0
    for rank in range(1, league.num_teams + 1):
        total_rankings[team][rank] = float(total_rankings[team][rank])/N
        avg_rank += float(rank)*float(total_rankings[team][rank])
        new_row.append(total_rankings[team][rank])
    new_row.append(avg_rank)
    new_row.append(str(sum(total_rankings[team][j] for j in range(1, 7))*100) + '%')
    new_row.append(str(sum(total_rankings[team][j] for j in range(1, 3))*100) + '%')
    table.append(new_row)

sorted_table = sorted(table, key=operator.itemgetter(15))
headers = ['team_(N=%s)' % N] + range(1, league.num_teams + 1) + ['Avg_Rank'] + ['%_Playoffs', '%_Rd1_Bye']
print '\n'
beesh.PrintTabularResults(headers, sorted_table)