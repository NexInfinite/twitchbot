import logging
import socket
from urllib.request import urlopen
from json import loads


class IRC:
    user_check = False
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, server, port, nick, channel, auth):
        self.server = server
        self.port = port
        self.nick = nick
        self.channel = channel
        self.auth = auth

    def get_msg(self):
        response = self.irc.recv(2048).decode().strip('\r\n')
        print(response)
        try:
            user, msg = response.split(':', 2)[1:]
            return self.get_user_from_msg(user), msg
        except ValueError:
            return '', response

    def format_msg(self, msg: str):
        formatted_msg = f'PRIVMSG #{self.channel} :{msg}\r\n'
        return formatted_msg.encode()

    def format_dm_msg(self, msg: str, user: str):
        formatted_msg_dm = f'PRIVMSG #{self.channel} : /w {user} {msg}'
        return formatted_msg_dm.encode()

    def ping(self):
        self.irc.send(b'PONG :tmi.twitch.tv\r\n')

    def send(self, msg):
        if isinstance(msg, bytes):
            msg = msg.decode('utf-8')

        formatted_msg = self.format_msg(msg)
        print(formatted_msg)
        self.irc.send(self.format_msg(msg))

    def send_dm(self, msg, user):
        if isinstance(msg, bytes):
            msg = msg.decode('utf-8')

        if isinstance(user, bytes):
            user = user.decode('utf-8')

        formatted_msg_dm = self.format_dm_msg(msg, user)
        print(formatted_msg_dm)
        self.irc.send(self.format_dm_msg(user, msg))

    @staticmethod
    def get_user_from_msg(user):
        return user.split('!')

    def connect(self):
        password = f'PASS {self.auth}\r\n'.encode()
        nick = f'NICK {self.nick}\r\n'.encode()
        channel = f'JOIN #{self.channel}\r\n'.encode()
        perm = f'CAP REQ :twitch.tv/commands\r\n'.encode()

        self.irc.connect((self.server, self.port))
        self.irc.send(password)
        self.irc.send(nick)
        self.irc.send(channel)
        self.irc.send(perm)

    def diconnect(self):
        self.irc.send(f'PART #{self.channel}'.encode())
        logging.info(f'disconnected from channel {self.channel}')

    def get_mods(self):
        response = urlopen('https://tmi.twitch.tv/group/user/nex_infinite/chatters')
        readable = response.read().decode('utf-8')
        chatlist = loads(readable)
        chatters = chatlist['chatters']
        moderators = chatters['moderators']
        return moderators
