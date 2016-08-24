__author__ = 'brendan'

import operator
import beesh


list_of_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF', 'D', 'DB']

class Draft:

    def __init__(self, available_players, roster):

        self.available_players = available_players  # { pos: {player : season_total} }
        self.roster = roster

    def show_available_players(self):

        positions = self.available_players.keys()
        max_remaining = max([len(self.available_players[pos]) for pos in self.available_players.keys()])

        table = []
        tabledict = {}
        for i in range(max_remaining):
            new_row = [i]
            for pos in positions:
                try:
                    new_row.append(self.available_players[pos].keys()[i].name)
                    tabledict[(i, pos)] = self.available_players[pos].keys()[i]
                except IndexError:
                    new_row.append('')
            table.append(new_row)
        beesh.PrintTabularResults(positions, table)

        return tabledict

    def remove_available_player(self, player):
        for pos in self.available_players.keys():
            try:
                del self.available_players[pos][player]
            except KeyError:
                pass

    def add_player_to_roster(self, player):
        self.roster.add_player(player)

    def top_n_additions(self, n=50):

        current_performance = self.roster.get_team_projection(self.roster.players)

        # Create dict of players sorted by season projection
        sorted_pos = {}
        # for pos in self.roster.starting_pos:
        for pos in list_of_positions:
            sorted_pos[pos] = sorted(self.available_players[pos].items(), key=operator.itemgetter(1), reverse=True)

        top_additions = {}
        for pos in list_of_positions:

            additions = []
            for i in range(len(sorted_pos[pos])):  # Take the top n performers in each position
                player_pts_tuple = sorted_pos[pos][i]
                roster_players_plus_player = self.roster.players + [player_pts_tuple[0]]
                team_projection = self.roster.get_team_projection(roster_players_plus_player)
                improvement = int(team_projection - current_performance)
                additions.append((improvement, player_pts_tuple[0]))
                if pos in ['QB', 'TE', 'K', 'DEF', 'DB']:
                    for second_player_pts_tuple in sorted_pos[pos][i+1:]:
                        if second_player_pts_tuple is player_pts_tuple:
                            pass
                        else:
                            second_roster_players_plus_player = self.roster.players + [player_pts_tuple[0],
                                                                                       second_player_pts_tuple[0]]
                            second_team_projection = self.roster.get_team_projection(second_roster_players_plus_player)
                            second_improvement = int(second_team_projection - current_performance)
                            additions.append((second_improvement, player_pts_tuple[0], second_player_pts_tuple[0]))

            sorted_additions = sorted(additions, reverse=True)

            top_additions[pos] = {}
            for i in range(n):
                try:
                    if len(sorted_additions[i]) == 3:
                        top_additions[pos][i] = (sorted_additions[i][1], sorted_additions[i][2], sorted_additions[i][0])
                    else:
                        top_additions[pos][i] = (sorted_additions[i][1], sorted_additions[i][0])
                except KeyError:
                    top_additions[pos][i] = ('N/A', 0)
                except IndexError:
                    top_additions[pos][i] = ('N/A', 0)
        return top_additions

    def top_additions(self):
        current_performance = self.roster.get_team_projection(self.roster.players)
        singles = {pos: {} for pos in list_of_positions}
        combos = {pos: {} for pos in list_of_positions}
        everyone = {pos: {} for pos in list_of_positions}
        pos_for_combos = ['QB', 'TE', 'K', 'DEF', 'DB']
        for pos in list_of_positions:
            for i in range(len(self.available_players[pos].keys())):
                player = self.available_players[pos].keys()[i]
                roster_plus_player = self.roster.players + [player]
                singles[pos][(player)] = self.roster.get_team_projection(roster_plus_player) - current_performance
                everyone[pos][(player)] = self.roster.get_team_projection(roster_plus_player) - current_performance

                if pos in pos_for_combos:
                    for j in range(i+1, len(self.available_players[pos].keys())):
                        second_player = self.available_players[pos].keys()[j]
                        if second_player != player:
                            roster_plus_second_player = roster_plus_player + [second_player]
                            combos[pos][(player, second_player)] = \
                                self.roster.get_team_projection(roster_plus_second_player) - current_performance
                            everyone[pos][(player, second_player)] = \
                                self.roster.get_team_projection(roster_plus_second_player) - current_performance

        best_players = {}
        sorted_indiv = {}
        next_best_combo = {}
        for pos in list_of_positions:
            sorted_singles = sorted(singles[pos].items(), key=operator.itemgetter(1), reverse=True)
            best_player = sorted_singles[0][0]
            best_player_value = sorted_singles[0][1]
            best_players[pos] = best_player
            sorted_indiv[pos] = sorted_singles
            sorted_combos = sorted(combos[pos].items(), key=operator.itemgetter(1), reverse=True)
            last_combo = None
            for combo in sorted_combos:
                value = combo[1]
                if value > best_player_value and best_player not in combo[0]:
                    last_combo = combo[1]  # TODO: update with average draft pick
                elif value > best_player_value:
                    pass
                else:
                    break
            next_best_combo[pos] = last_combo


        top_additions = {}
        for pos in list_of_positions:
            top_additions[pos] = {}
            rank = 0
            for tup in sorted(everyone[pos].items(), key=operator.itemgetter(1), reverse=True):
                try:
                    if best_players[pos] in tup[0]:
                        del everyone[pos][tup[0]]
                    else:
                        top_additions[pos][rank] = (list(tup[0]), tup[1])
                        rank += 1
                except TypeError:
                    top_additions[pos][rank] = ([tup[0]], tup[1])
                    rank += 1
        return top_additions, sorted_indiv, next_best_combo


    def show_top_additions(self, n=10):

        top_additions, sorted_singles, next_best_combo = self.top_additions()
        table = []
        top_table = []
        max_rank = max(len(top_additions[pos].keys()) for pos in top_additions.keys())

        for i in range(max_rank):
            new_row = [i]
            if i < n:
                new_top_row = [i]

            for pos in list_of_positions:
                try:
                    performance = int(top_additions[pos][i][1])
                    performance_above_best = int(performance - top_additions[pos][0][1])
                    players = top_additions[pos][i][0]
                    new_row.append('%s - %s' % (performance_above_best, tuple(players)))

                except KeyError:
                    new_row.append('')

                if i < n:
                    try:
                        top_player, top_performance = sorted_singles[pos][i]
                        top_above_best = top_performance - sorted_singles[pos][0][1]
                        if i == 0:
                            new_top_row.append('%s - %s (%s)' % (top_performance, top_player, next_best_combo[pos]))
                        else:
                            new_top_row.append('%s - %s' % (top_above_best, top_player))
                    except KeyError:
                        new_top_row.append('')

            if i < n:
                top_table.append(new_top_row)
            if (i+1) % 3 == 0 and 0 < i < n:
                top_table.append(['' for element in new_top_row])
            table.append(new_row)

        print "~~~~~~~~~~~~~~~~ THE BOARD ~~~~~~~~~~~~~~~~"
        beesh.PrintTabularResults([''] + list_of_positions, table[::-1])
        print '\n'

        print "~~~~~~~~~~~~~~~~ TOP %s ~~~~~~~~~~~~~~~~" % n
        beesh.PrintTabularResults([''] + list_of_positions, top_table)
        print '\n'
        return top_additions