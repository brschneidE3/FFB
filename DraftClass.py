__author__ = 'brendan'

import operator
import beesh

list_of_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']

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
        # for pos in self.roster.starting_pos:
        for pos in list_of_positions:
            top_additions[pos] = {}
            additions = []
            for player_pts_tuple in sorted_pos[pos][:n]:  # Take the top n performers in each position
                roster_players_plus_player = self.roster.players + [player_pts_tuple[0]]
                team_projection = self.roster.get_team_projection(roster_players_plus_player)
                improvement = int(team_projection - current_performance)
                additions.append((improvement, player_pts_tuple[0]))
            sorted_additions = sorted(additions, reverse=True)

            for i in range(n):
                try:
                    top_additions[pos][i] = (sorted_additions[i][1], sorted_additions[i][0])
                except KeyError:
                    top_additions[pos][i] = (0, 'N/A')
                except IndexError:
                    top_additions[pos][i] = (0, 'N/A')

        return top_additions

    def show_top_n_additions(self, additions_to_calc, additions_to_show):

        top_n_additions = self.top_n_additions(additions_to_calc)
        top_dict = {}

        table = []

        for i in range(additions_to_show):
            new_row = [i]
            for pos in list_of_positions:
                if i == 0:
                    new_row.append('%s - %s' % (top_n_additions[pos][i][1], top_n_additions[pos][i][0]))
                else:
                    new_row.append('%s (%s) - %s' % (top_n_additions[pos][i][1],
                                                     top_n_additions[pos][i][1] - top_n_additions[pos][i-1][1],
                                                     top_n_additions[pos][i][0]))
            top_dict[(i, pos)] = top_n_additions[pos][i][0]
            table.append(new_row)

        beesh.PrintTabularResults(list_of_positions, table)
        return top_dict
