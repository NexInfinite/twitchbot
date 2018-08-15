from No3rdPartLibTwitchBot import *
from configno3rdparty import *
from SQLiteCommands import *
import shlex
from Custom_Permissions_config_final import *
from SQLiteCommandsForGroups import *
import time
import os

AUTH = os.getenv('oauth')
SERVER = os.getenv('server')
PORT = os.getenv('port')
CHANNEL = os.getenv('channel')
NICK = os.getenv('nickname')

response = None
response_dm = None
response_dm_other = None
response_2 = None
user = ''
msg = ''
split_message = shlex.split(msg)
n = 0
reload = False

def main(irc):
    if AUTH is None:
        print("ERROR! You did not provide a AUTH key")

    running = True

    irc.send('Hello streamer, How are you today?')

    moderators = irc.get_mods()

    while running:
        global response, n, response_dm, response_dm_other, response_2, reload
        user, msg = irc.get_msg()

        try:
            split_message = shlex.split(msg)
        except:
            split_message = msg.split(' ')


        if msg == 'PING :tmi.twitch.tv':
            irc.ping()

        if msg.startswith('?userman'):
            print("all good here")
            response = f'Userman????? More like HelperMan'

        if msg.startswith('?sudokid'):
            response = f'SudoKid?!?!?!? Never heard of him?'

        if msg.startswith('hello'):
            response = f'Hello @{user[0]}, how are you today?'

        if msg.startswith('?ceaser'):
            response = f'Salad?'

        if msg.startswith('help'):
            if len(split_message) < 2:
                response_dm = f'@{user[0]} You need to specify the command you would like help on (?addcom, ?delcom, ?editcom, ?addperm, ?delperm, ?adduser, ?deluser, ?addgroup, ?delgroup, ?timeout, ?untimeout, ?mod, ?unmod ?addcomp)'
                pass
            else:
                if split_message[1] == '?addcom':
                    response_dm = f'@{user[0]}, To use ?addcom you must be a mod, if you are the use: ?addcom <command> <response>'
                elif split_message[1] == '?editcom':
                    response_dm = f'@{user[0]}, To use ?editcom you must be a mod, if you are then use: ?editcom <command> <new_response>'
                elif split_message[1] == '?delcom':
                    response_dm = f'@{user[0]}, To use ?delcom You must be a mod, if you are then use: ?delcom <command>'
                elif split_message[1] == '?addperm':
                    response_dm = f'@{user[0]}, To use ?addperm You must be a admin, if you are then use: ?addperm <group> <permission>'
                elif split_message[1] == '?delperm':
                    response_dm = f'@{user[0]}, To use ?delperm You must be a admin, if you are then use: ?delperm <group> <permission>'
                elif split_message[1] == '?adduser':
                    response_dm = f'@{user[0]}, To use ?adduser You must be a admin, if you are then use: ?adduser <group> <user>'
                elif split_message[1] == '?deluser':
                    response_dm = f'@{user[0]}, To use ?deluser You must be a admin, if you are then use: ?deluser <group> <user>'
                elif split_message[1] == '?addgroup':
                    response_dm = f'@{user[0]}, To use ?addgroup You must be a admin, if you are then use: ?addgroup <group> <permissions>'
                elif split_message[1] == '?delgroup':
                    response_dm = f'@{user[0]}, To use ?delgroup You must be a admin, if you are then use: ?delgroup <group>'
                elif split_message[1] == '?timeout':
                    response_dm = f'@{user[0]}, To use ?timeout You must be a mod, if you are then use: ?timeout <user> <time(levae blank for 5 minutes)>'
                elif split_message[1] == '?untimeout':
                    response_dm = f'@{user[0]}, To use ?untimeout You must be a mod, if you are then use: ?addgroup <user>'
                elif split_message[1] == '?mod':
                    response_dm = f'@{user[0]}, To use ?mod You must be the admin, if you are then use: ?mod <user>'
                elif split_message[1] == '?unmod':
                    response_dm = f'@{user[0]}, To use ?unmod You must be a admin, if you are then use: ?unmod <user>'
                elif split_message[1] == '?addcomp':
                    response_dm = f'@{user[0]}, To use ?addcomp You must be a mod, if you are then use: ?addcomp <command> <response> <group permission>'

        if msg.startswith('?addcom'):
            resp_ = test_all_groups_for_perm(user[0], 'mods')
            if resp_:
                split_message = shlex.split(msg)
                if len(split_message) < 2:
                    response = f'@{user[0]} invalid arguments: ?addcom <command> <response>'
                    pass
                else:
                    resp = insert_cmd(
                        command_given=split_message[1],
                        response_given=split_message[2:],
                    )
                    if resp == 2:
                        response = f'@{user[0]} You may not overide the {split_message[1]} command. Kappa'
                    elif resp == True:
                        response = f'@{user[0]}, the command {split_message[1]} has been added. The response is: {" ".join(split_message[2:])}'
                    else:
                        response = f'@{user[0]} The command {split_message[1]} has already been created! Use ?editcom to edit the command.'
            else:
                response = f'@{user[0]}, you are not a mod/admin. Sorry but you cannot add commands!'

        if msg.startswith('?delcom'):
            resp_ = test_all_groups_for_perm(user[0], 'mods')
            if resp_:
                split_message = shlex.split(msg)
                if len(split_message) < 2:
                    response = f'@{user[0]} invalid arguments: ?delcom <command>. For example ?delcom ?example'
                    pass
                else:
                    resp = delete_command_from_database(
                        command=split_message[1]
                    )
                    if resp:
                        response = f'@{user[0]} The command {split_message[1]} has been found and deleted!'
                    else:
                        response = f'@{user[0]} The command {split_message[1]} has not command has been found!'
            else:
                response = f'@{user[0]}, You are not a mod, this means you cannot delete commands'

        if msg.startswith('?editcom'):
            resp_ = test_all_groups_for_perm(user[0], 'mods')
            if resp_:
                split_message = shlex.split(msg)
                if len(split_message) < 2:
                    response = f'Invalid arguments: ?editcom <command> <new_response>. For example ?editcom ?example This is another example. Also make sure the command name is not changed, You cannot do that'
                    pass
                else:
                    resp = edit_command_in_database(
                        command=split_message[1],
                        response=split_message[2:]
                    )
                    if resp:
                        response = f'@{user[0]} The command {split_message[1]} has been updated, the new response is now {" ".join(split_message[2:])}'
                    else:
                        response = f'@{user[0]} This command does not exist. Use ?addcom to add it.'
            else:
                response = f'@{user[0]}, You are not a mod on the channel, you cannot add the command'

        if msg.startswith('?timeout'):
            resp_ = test_all_groups_for_perm(user[0], 'mod')
            if resp_:
                if len(split_message) < 2:
                    response = f'{user[0]} Invalid arguments: ?timeout <user> <time>(if no time then a 5 minute timeout)'
                    response_2 = f'@{split_message[1]} has been timed out for 600 seconds!'
                elif len(split_message) < 3:
                    response = f'/timeout {split_message[1]}'
                    response_2 = f'@{split_message[1]} has been timed out for 600 seconds!'
                elif len(split_message) > 2:
                    response = f'/timeout {split_message[1]} {split_message[2]}'
                    response_2 = f'The user {split_message[1]} has been timed out for {split_message[2]} seconds!'
            else:
                response = f'@{user[0]}, You are not a mod on the channel, you cannot add the command'

        if msg.startswith('?untimeout'):
            resp_ = test_all_groups_for_perm(user[0], 'mod')
            if user[0] in moderators:
                if len(split_message) < 2:
                    response = f'@{user[0]} Invalid arguments: ?timeout <user>'
                elif len(split_message) < 3:
                    response = f'/untimeout {split_message[1]}'
                    response_2 = f'The user {split_message[1]} is no longer timed out from this channel!'
                else:
                    response = f'@{user[0]}, You are not a mod on the channel, you cannot add the command'

        if msg.startswith('?addgroup'):
            resp_ = test_all_groups_for_perm(user[0], 'admin')
            if resp_:
                if len(split_message) < 3:
                    response = f'@{user[0]} Invalid arguments: ?addgroup <group> <permissions>'
                else:
                    resp = add_group(
                        group=split_message[1],
                        permss=split_message[2]
                    )
                    if resp:
                        response = f'Added {split_message[1]} to the database! The permissions are {split_message[2]}'
                    else:
                        response = f'Group {split_message[1]} is already in the database!'
            else:
                response = f'@{user[0]}, You are not a admin on the channel, you cannot add the command'

        if msg.startswith('?delgroup'):
            resp_ = test_all_groups_for_perm(user[0], 'admin')
            if resp_:
                if len(split_message) < 2:
                    response = f'@{user[0]} Invalid arguments: ?delgroup <group>'
                else:
                    resp = del_group(
                        groupp=split_message[1]
                    )
                    if resp:
                        response = f'Group deleted!'
                    else:
                        response = f'Group "{split_message[1]}" is not in the database!'
            else:
                response = f'@{user[0]}, You are not a admin on the channel, you cannot add the command'

        if msg.startswith('?adduser'):
            resp_ = test_all_groups_for_perm(user[0], 'admin')
            if resp_:
                if len(split_message) < 2:
                    response = f'@{user[0]} Invalid arguments: ?adduser <group> <user>'
                else:
                    resp = add_user_to_group(
                        user=split_message[2],
                        group=split_message[1]
                    )
                    if resp:
                        response = f'Added "{split_message[2]}" to the group "{split_message[1]}"!'
                    else:
                        response = f'user "{split_message[2]}" is already in the group "{split_message[1]}"!'
            else:
                response = f'@{user[0]}, You are not a admin on the channel, you cannot add the command'

        if msg.startswith('?deluser'):
            resp_ = test_all_groups_for_perm(user[0], 'admin')
            if resp_:
                if len(split_message) < 3:
                    response = f'@{user[0]} Invalid arguments: ?deluser <group> <user>'
                else:
                    resp = delete_user(
                        user=split_message[2],
                        group=split_message[1]
                    )
                    if resp:
                        response = f'The user "{split_message[2]}" is now deleted from group "{split_message[1]}"!'
                    else:
                        response = f'There was an error, either the group "{split_message[1]}" does not exist or the user "{split_message[2]}" does not exist in that group!'
            else:
                response = f'@{user[0]}, You are not a admin on the channel, you cannot add the command'

        if msg.startswith('?addperm'):
            resp_ = test_all_groups_for_perm(user[0], 'admin')
            if resp_:
                if len(split_message) < 3:
                    response = f'@{user[0]} Invalid arguments: ?addperm <group> <permission>'
                else:
                    resp = add_perm(
                        permss=split_message[2],
                        group=split_message[1]
                    )
                    if resp:
                        response = f'The permission "{split_message[2]}" is now added to the group "{split_message[1]}"!'
                    else:
                        response = f'There was an error, either the group "{split_message[1]}" does not exist or the permission "{split_message[2]}" already exists in the group!'
            else:
                response = f'@{user[0]}, You are not an admin on the channel, you cannot add the command'

        if msg.startswith('?delperm'):
            resp_ = test_all_groups_for_perm(user[0], 'admin')
            if resp_:
                if len(split_message) < 3:
                    response = f'@{user[0]} Invalid arguments: ?delperm <group> <permission>'
                else:
                    resp = del_perm(
                        permss=split_message[2],
                        group=split_message[1]
                    )
                    if resp:
                        response = f'The permission "{split_message[2]}" has been deleted from the group "{split_message[1]}"!'
                    else:
                        response = f'There was an error, either thr group "{split_message[1]}" does not exist or the permission "{split_message[2]}" already exists!'
            else:
                response = f'@{user[0]}, You are not a admin on the channel, you cannot add the command'

        if msg.startswith('?mod'):
            resp_ = test_all_groups_for_perm(user[0], 'admin')
            if resp_:
                if len(split_message) > 2:
                    response = f'cmonBruh You are admins its ?mod <user>'
                else:
                    user_ = split_message[1]
                    add_user_to_group(user_, 'mods')
                    response = f'/mod {split_message[1]}'
                    response_dm_other = f'You are now mod {split_message[1]}! Congrats'
            else:
                response = f'@{user[0]}, You are not the leader on the channel, you cannot use this command sorry'

        if msg.startswith('?unmod'):
            resp_ = test_all_groups_for_perm(user[0], 'admin')
            if resp_:
                if len(split_message) > 2:
                    response = f'cmonBruh You are admins its ?unmod <user>'
                else:
                    user_ = split_message[1]
                    delete_user({user_[1]}, 'mods')
                    response = f'/unmod {split_message[1]}'
                    response_dm_other = f'{split_message[1]} Your mod has been taken away, {user[0]} did it ask him why'
            else:
                response = f'@{user[0]}, You are not the leader on the channel, you cannot use this command sorry'

        if msg.startswith('?addcomp'):
            resp_ = test_all_groups_for_perm(user[0], 'mod')
            if resp_:
                if len(split_message) < 4:
                    response = f'Invalid arguments: ?addcomp <command> <response> <permission group>'
                else:
                    resp = insert_into_table(
                        command=split_message[1],
                        response=split_message[2:-1],
                        perm=split_message[-1]
                    )
                    if resp == 0:
                        response = f'@{user[0]} The command {split_message[1]} has been created and can only be use for the group {split_message[-1]}. The response is {" ".join(split_message[2:-1])}!'
                    elif resp == 1:
                        response = f'@{user[0]} The command {split_message[1]} has already been created for everyone to use, delete this command if you want to make it specific to a group!'
                    elif resp == 2:
                        response = f'@{user[0]} you are not allowed to make command that are "?sudokid" , "?userman" or "help"'
                    elif resp == 3:
                        response = f'@{user[0]} The command {split_message[1]} has already been created!'
            else:
                response = f'@{user[0]} You are not a mod on this channel, you cannot use this command'

        if msg.startswith('reload'):
            resp_ = test_all_groups_for_perm(user[0], 'mods')
            if resp_:
                irc_server = IRC(SERVER, PORT, NICK, CHANNEL, AUTH)
                if reload == False:
                    irc_server.diconnect()
                    reload = True
                if reload == True:
                    main(irc_server)
                    continue
            else:
                response = f'@{user[0]} You are not a mod on this channel. You cannot use this command!'

        resp = get_command_response(split_message[0])
        resp_2 = get_response_from_command(split_message[0])

        if resp_2 is not None:
            if test_all_groups_for_perm(user[0], resp_2[-1]):
                response = resp_2[1]
            else:
                response = f'@{user[0]} You do not have the permission of "{resp_2[-1]}"'

        if resp is not None:
            response = resp

        if response_dm is not None:
            irc.send_dm(response_dm, user[0])
            response_dm = None

        if response_dm_other is not None:
            irc.send_dm(response_dm_other, user[0])
            response_dm_other = None

        if response is not None:
            irc.send(response)
            response = None

        if response_2 is not None:
            irc.send(response_2)
            response_2 = None


if __name__ == '__main__':
    irc_server = IRC(SERVER, PORT, NICK, CHANNEL, AUTH)
    irc_server.connect()

    try:
        main(irc_server)
    except KeyboardInterrupt:
        irc_server.diconnect()
