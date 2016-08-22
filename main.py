__author__ = 'brsch'

import read_data
import operator
import RosterClass

available_players = read_data.read()
roster = RosterClass.Roster()

import DraftClass
draft = DraftClass.Draft(available_players, roster)


def add_player(roster, draft, pos_to_add):
    status = 'asking'

    while status is 'asking':
        addable_players = sorted(draft.available_players[pos_to_add].items(), key=operator.itemgetter(1), reverse=True)
        player_dict = {}
        for i in range(len(addable_players)):
            player_dict[i] = addable_players[i][0]
            print i, player_dict[i]

        try:
            i_player = int(raw_input('Enter number beside player to DRAFT: '))
        except:
            return roster, draft

        try:
            player_to_add = player_dict[i_player]
        except:
            return roster, draft

        confirm = raw_input('Did you mean to DRAFT %s? (y/n) ' % player_to_add)
        if confirm == 'y':
            status = 'adding'
        else:
            return roster, draft

    roster.add_player(player_to_add)
    draft.remove_available_player(player_to_add)
    print 'Added %s to roster!' % player_to_add
    print roster.players
    return roster, draft


def remove_player(roster, draft, pos_to_remove):
    status = 'asking'

    while status is 'asking':
        removable_players = \
            sorted(draft.available_players[pos_to_remove].items(), key=operator.itemgetter(1), reverse=True)
        player_dict = {}
        for i in range(len(removable_players)):
            player_dict[i] = removable_players[i][0]
            print i, player_dict[i]

        try:
            i_player = int(raw_input('Enter number beside player to REMOVE: '))
        except:
            return roster, draft

        try:
            player_to_remove = player_dict[i_player]
        except:
            return roster, draft

        confirm = raw_input('Did you mean to REMOVE %s? (y/n) ' % player_to_remove)
        if confirm == 'y':
            status = 'adding'
        else:
            return roster, draft

    draft.remove_available_player(player_to_remove)
    print 'Removed %s!' % player_to_remove
    return roster, draft

status = 'drafting'
while status is 'drafting':

    top_additions = draft.show_top_additions()
    command = raw_input('Options: draft(POS), remove(POS), done: ')

    if 'draft' in command:
        pos_to_add = command[6:-1]
        if pos_to_add in DraftClass.list_of_positions:
            roster, draft = add_player(roster, draft, pos_to_add)
    elif 'remove' in command:
        pos_to_remove = command[7:-1]
        if pos_to_remove in DraftClass.list_of_positions:
            roster, draft = remove_player(roster, draft, pos_to_remove)
    elif 'done' in command:
        status = 'done'
