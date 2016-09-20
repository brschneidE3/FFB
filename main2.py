__author__ = 'brendan'

import read
import beesh
import operator
import copy
import RosterClass


top_n_to_view = 13
players_on_team = []
# List of (Position, Rank) denoting players on roster
players_to_draft = [
    # Drafted
    ('TE', 12), ('RB', 13), ('D', 38), ('WR', 23), ('DEF', 3), ('DB', 12), ('QB', 22), ('WR', 68),
    ('RB', 46), ('K', 13), ('WR', 64), ('RB', 41), ('QB', 19), ('D', 28), ('D', 58), ('DEF', 19),
    # Acquired
    ('WR', 25)]

# List of (Position, Rank) denoting players taken off the board
players_to_remove = [('WR', 0), ('WR', 29), ('WR', 52), ('WR', 16),
                     ('TE', 19), ('RB', 2), ('RB', 15), ('RB', 57), ('WR', 2), ('WR', 14),
    ('RB', 24), ('WR', 44), ('WR', 5), ('RB', 43), ('RB', 25), ('WR', 8), ('TE', 8), ('WR', 36), ('RB', 40),
    ('WR', 33), ('RB', 31), ('WR', 6), ('RB', 47), ('RB', 18), ('WR', 4), ('WR',  1), ('RB', 42), ('WR', 20), ('QB', 9),
    ('WR', 56), ('WR', 30), ('QB', 2), ('WR', 62), ('RB', 5), ('WR', 67), ('WR', 13), ('WR', 18), ('WR', 31), ('QB', 28),
    ('WR', 21), ('RB', 44), ('RB', 6), ('WR', 37), ('RB', 45), ('WR', 27), ('WR', 3), ('DB', 32), ('DEF', 21), ('RB', 19),
    ('TE', 21), ('RB', 59), ('QB', 11), ('RB', 52), ('DEF', 6), ('D', 36), ('WR', 41), ('QB', 1), ('WR', 43), ('DEF', 0),
    ('QB', 7), ('RB', 33), ('DEF', 14), ('WR', 28), ('RB', 23), ('TE', 5), ('QB', 30), ('WR', 45), ('DB', 36), ('DEF', 11),
    ('WR', 32), ('QB', 24), ('WR', 22), ('RB', 16), ('RB', 38), ('WR', 59), ('DB', 15), ('DEF', 4), ('D', 46), ('WR', 46),
    ('K', 23), ('DEF', 12), ('RB', 35), ('TE', 13), ('TE', 2), ('DB', 18), ('D', 25), ('QB', 10), ('D', 0), ('WR', 17),
    ('DEF', 18), ('D', 8), ('D', 55), ('QB', 33), ('D', 5), ('RB', 27), ('D', 47), ('D', 11), ('WR', 24), ('D', 53),
    ('D', 33), ('RB', 1), ('TE', 7), ('D', 6), ('WR', 63), ('RB', 22), ('WR', 50), ('TE', 20), ('DB', 7), ('RB', 51),
    ('WR', 74), ('D', 23), ('D', 19), ('D', 15), ('D', 34), ('D', 39), ('DB', 29), ('WR', 19), ('TE', 11), ('DB', 14),
    ('WR', 40), ('WR', 60), ('TE', 23), ('RB', 14), ('D', 51), ('RB', 0), ('WR', 61), ('RB', 26), ('RB', 48), ('WR', 15),
    ('RB', 39), ('RB', 28), ('WR', 72), ('WR', 11), ('WR', 66), ('TE', 0), ('WR', 47), ('DEF', 9), ('DB', 24), ('DEF', 13),
    ('WR', 36), ('DEF', 17), ('D', 27), ('RB', 60), ('WR', 57), ('RB', 62), ('RB', 56), ('RB', 7), ('RB', 32), ('D', 35),
    ('QB', 12), ('D', 29), ('QB', 4), ('DB', 25), ('RB', 4), ('TE', 4), ('WR', 53), ('QB', 14), ('TE', 10), ('RB', 29),
    ('K', 24), ('RB', 9), ('WR', 48), ('QB', 18), ('WR', 69), ('RB', 20), ('RB', 8), ('WR', 73), ('RB', 36), ('QB', 21),
    ('TE', 1), ('WR', 65), ('RB', 54), ('DB', 27), ('WR', 39), ('WR', 70), ('D', 37), ('QB', 0), ('DB', 34), ('D', 20),
    ('DEF', 8), ('DB', 13), ('TE', 24), ('RB', 55), ('WR', 54), ('D', 31), ('RB', 12), ('WR', 49), ('K', 10), ('WR', 12),
    ('K', 4), ('TE', 14), ('RB', 21), ('D', 4), ('K', 2), ('K', 1), ('D', 21), ('WR', 71), ('RB', 37), ('RB', 50)
    ]

all_players, players_by_pos = read.read()
sorted_by_pos = {pos: [tup[0] for tup in sorted(players_by_pos[pos].items(), key=operator.itemgetter(1))]
                 for pos in players_by_pos.keys()}
largest_set = max([len(sorted_by_pos[pos]) for pos in sorted_by_pos.keys()])
available_by_pos = copy.copy(players_by_pos)

# Print the board of all NFL players
player_grid = []
headers = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF', 'D', 'DB']
for i in range(largest_set):
    new_row = []
    for position in headers[:]:
        try:
            new_row.append('(%s) %s - %s (%s)' % (i, sorted_by_pos[position][i].name[:10], sorted_by_pos[position][i].team, sorted_by_pos[position][i].total))
        except IndexError:
            new_row.append('')
    player_grid.append(new_row)
beesh.PrintTabularResults(headers, player_grid)
print '\n'


# Add all players to roster and remove them from the available player pool
for pos, rank in players_to_draft:
    player = sorted_by_pos[pos][rank]
    players_on_team.append(player)
    for pos in available_by_pos.keys():
        if player in available_by_pos[pos].keys():
            del available_by_pos[pos][player]
            print '%s added to roster' % player
print '\n'

# Remove all taken players from the available player pool
n = len(players_to_remove)
for pos, rank in players_to_remove:
    player = sorted_by_pos[pos][rank]
    for pos in available_by_pos.keys():
        if player in available_by_pos[pos].keys():
            del available_by_pos[pos][player]
            print '%s deleted from %s' % (player, pos)
print '\n'

roster = RosterClass.Roster(players_on_team)
current_projection = roster.performance

single_projections = {}
for position in available_by_pos.keys():
    single_projections[position] = {}
    for player in available_by_pos[position].keys():
        players_plus_new = roster.players + [player]
        temp_roster = RosterClass.Roster(players_plus_new)
        new_projection = temp_roster.performance
        improvement = new_projection - current_projection
        single_projections[position][player] = improvement

sorted_singles = {position: sorted(single_projections[position].items(), key=operator.itemgetter(1), reverse=True)
                  for position in single_projections.keys()}


table = []
header = ['i', 'QB', 'RB', 'WR', 'TE', 'K', 'DEF', 'D', 'DB']
for i in range(top_n_to_view):
    new_row = [i]
    for position in header[1:]:
        try:
            new_projection = sorted_singles[position][i][1]
            new_player = sorted_singles[position][i][0]
            best_projection = sorted_singles[position][0][1]
            compared_to_best = int(new_projection - best_projection)

            new_row.append('%s (%s) - %s' % (int(new_projection), compared_to_best, new_player))
        except IndexError:
            new_row.append('')
    table.append(new_row)
beesh.PrintTabularResults(header, table)
