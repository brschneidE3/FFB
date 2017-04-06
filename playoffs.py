__author__ = 'brendan'

from numpy.random import normal
from numpy import average
from operator import itemgetter
import beesh
from load_data import dict_of_teams
import math
from TeamClass import League

league = League(dict_of_teams)
N = 10000
seeds = {}
end_of_year_standings = league.get_standings()
for seed in end_of_year_standings.keys():
    if seed <= league.top_n_makeplayoffs:
        team_name = end_of_year_standings[seed][0]
        seeds[team_name] = seed
        seeds[seed] = team_name

# Season results
weights = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
avgs = {}
sds = {}
for team_name in dict_of_teams.keys():
    avgs[team_name] = average([dict_of_teams[team_name].performance[i] for i in range(1, 14)], weights=weights)
    variances = [(dict_of_teams[team_name].performance[i] - avgs[team_name])**2 for i in range(1, 14)]
    var = average(variances, weights=weights)
    sds[team_name] = math.sqrt(var)

championship_wins = {seed: 0 for seed in seeds.keys()}
championship_appearances = {seed: 0 for seed in seeds.keys()}

for i in range(N):
    round_1_winners = [1, 2]
    # Round 1
    seed_3_score = normal(avgs[seeds[3]], sds[seeds[3]], 1)[0]
    seed_4_score = normal(avgs[seeds[4]], sds[seeds[4]], 1)[0]
    seed_5_score = normal(avgs[seeds[5]], sds[seeds[5]], 1)[0]
    seed_6_score = normal(avgs[seeds[6]], sds[seeds[6]], 1)[0]

    if seed_3_score > seed_6_score:
        round_1_winners.append(3)
    else:
        round_1_winners.append(6)
    if seed_4_score > seed_5_score:
        round_1_winners.append(4)
    else:
        round_1_winners.append(5)

    # Round 2
    if 3 in round_1_winners and 4 in round_1_winners:
        round_2_matchups = [(2, 3), (1, 4)]
    elif 3 in round_1_winners and 5 in round_1_winners:
        round_2_matchups = [(2, 3), (1, 5)]
    elif 6 in round_1_winners and 4 in round_1_winners:
        round_2_matchups = [(2, 4), (1, 6)]
    else:
        round_2_matchups = [(1, 6), (2, 5)]

    championship_teams = []
    for team1, team2 in round_2_matchups:
        team1_score = normal(avgs[seeds[team1]], sds[seeds[team1]], 1)[0]
        team2_score = normal(avgs[seeds[team2]], sds[seeds[team2]], 1)[0]
        if team1_score > team2_score:
            championship_teams.append(team1)
            championship_appearances[team1] += 1
        else:
            championship_teams.append(team2)
            championship_appearances[team2] += 1

    # Round 3
    champ_scores = []
    for team in championship_teams:
        team_score = normal(avgs[seeds[team]], sds[seeds[team]], 1)[0]
        champ_scores.append(team_score)

    if champ_scores[0] > champ_scores[1]:
        winner = championship_teams[0]
    else:
        winner = championship_teams[1]

    championship_wins[winner] += 1

p_champion = {}
p_inship = {}
for key in championship_wins.keys():
    try:
        int(key)
        name_of_seed = seeds[key]
        p_champion[name_of_seed] = float(championship_wins[key])/float(N)
        p_inship[name_of_seed] = float(championship_appearances[key]) / float(N)
    except ValueError:
        pass
sorted_p_champions = sorted(p_champion.items(), key=itemgetter(1), reverse=True)
sorted_p_inship = sorted(p_inship.items(), key=itemgetter(1), reverse=True)
for i in range(len(sorted_p_champions)):
    row = sorted_p_champions[i]
    new_row = [row[0], '%s%%' % (row[1]*100)]
    sorted_p_champions[i] = new_row

    row = sorted_p_inship[i]
    new_row = [row[0], '%s%%' % (row[1]*100)]
    sorted_p_inship[i] = new_row

beesh.PrintTabularResults(['Team', '% Win Championship'], sorted_p_champions)
print '\n'
beesh.PrintTabularResults(['Team', '% Makes Championship'], sorted_p_inship)