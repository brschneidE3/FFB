__author__ = 'brsch'

import read_data
import RosterClass

available_players = read_data.read()
roster = RosterClass.Roster()
# weekly_performance = roster.calc_weekly_performance(roster.players)
# roster.show_weekly_performance(weekly_performance)

import DraftClass
draft = DraftClass.Draft(available_players, roster)

# top_dict = draft.show_top_n_additions(additions_to_calc=1000,
#                                       additions_to_show=630)
#
# status = 'drafting'
#
# while status == 'drafting':
#
#     the_board = draft.show_top_n_additions(additions_to_calc=1000,
#                                            additions_to_show=861)
#
#
#     status = 'done'

draft.show_top_additions(10)
