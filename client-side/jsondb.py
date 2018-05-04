'''
/*
API:


*/
'''
from hashlib import md5
from json import loads, dumps
from crypter import passwd_decode, passwd_encode
from base64 import b64encode, b64decode, urlsafe_b64encode, urlsafe_b64decode


class JsonDataBase:
    def __init__(self, passwd):
        self.db = None
        self.__passwd = passwd

    def __repr__(self):
        return 'nick:{0}\nuser_id:{1}\nsession_key:{2}\ncontacts:{3}\nchats:{4}\nsettings:{5}'.format(self.nick, self.user_id, self.session_key, self.contacts, self.chats, self.settings)

    def read(self):
        if not self.db:
            self.db = open('db.json')
            data = self.db.read()
            self.db.close()
            self.db = None
            
        else:
            return 'DB already was opened'
        try:
            data = loads(passwd_decode(self.__passwd, data))
        except:
            return 'invalid password'
        self.nick = data['nickname']
        self.user_id = data['id']
        self.session_key = data['session_key']
        self.contacts = data['contacts']
        self.chats = data['chats']
        self.settings = data['settings']
        return "successfull"


    def write(self):
        if not self.db:
            data = dumps({
                'contacts': self.contacts,
                'session_key': self.session_key,
                'id': self.user_id,
                'nickname': self.nick,
                'chats': self.chats,
                'settings': self.settings
            })
            data = passwd_encode(self.__passwd, data)
            try:
                self.db = open('db.json', 'w')

            except:
                return 'DB already was opened'

            self.db.write(data)
            self.db.close()
            self.db = None
            return 'successfull'

        else:
            return 'DB already was opened'

            
    def create_db(self, nick, user_id, session_key, contacts, chats, settings):
        self.nick = nick
        self.user_id = user_id
        self.session_key = session_key
        self.contacts = contacts
        self.chats = chats
        self.settings = settings
        self.write()

    def update_session_key(self, key):
        if not self.db:
            self.read()
        self.session_key = key
        answ = self.write()
        return 'successfull' if answ == 'successfull' else 'error'

    def create_chat(self, chat_id):
        if not self.db:
            self.read()
        self.chats[chat_id] = {'sending_chain': [], 'main_chain': []}
        answ = self.write()
        return 'successfull' if answ == 'successfull' else 'error'

    def append_snd_msg(self, chat_id, msg_id,msg):
        if not self.db:
            self.read()
        self.chats[chat_id]['sending_chain'].append({'msg_id': msg_id, 'msg': msg})
        answ = self.write()
        return 'successfull' if answ == 'successfull' else 'error'

    def append_sent_msg(self, chat_id, msg_id):
        if not self.db:
            self.read()
        for i in self.chats[chat_id]['sending_chain']:
            if i['msg_id'] == msg_id:
                break
        self.chats[chat_id]['main_chain'].append(i)
        self.chats[chat_id]['sending_chain'].remove(i)
        answ = self.write()
        return 'successfull' if answ == 'successfull' else 'error'

    def append_got_msg(self, chat_id, msg_id, msg, date):
        if not self.db:
            self.read()        
        for i in self.chats[chat_id]['main_chain']:
            if i['msg_id'] == msg_id:
                return 'already have'
        self.chats[chat_id]['main_chain'].append({'msg_id': msg_id, 'msg': msg, 'from': 1, 'date': date})
        answ = self.write()
        return 'successfull' if answ=='successfull' else 'error'

    def delete_chat(self, chat_id):
        pass

