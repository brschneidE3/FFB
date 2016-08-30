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
    ]
# List of (Position, Rank) denoting players taken off the board
players_to_remove = [
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
            new_row.append('(%s) %s - %s ' % (i, sorted_by_pos[position][i].name, sorted_by_pos[position][i].team))
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
