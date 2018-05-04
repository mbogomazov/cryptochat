from base64 import b64encode, b64decode, urlsafe_b64encode, urlsafe_b64decode
from time import time
from random import randint
from hashlib import md5
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):
    def __init__(self, key):
        self.key = key
        self.BS = 16
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) \
            * chr(self.BS - len(s) % self.BS).encode()
        self.unpad = lambda s: s[:-ord(s[len(s)-1:])]

    def encrypt(self, message):
        raw = self.pad(message)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv())
        enc = cipher.encrypt(raw)
        return b64encode(enc)

    def decrypt(self, enc):
        enc = b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv())
        dec = cipher.decrypt(enc)
        return self.unpad(dec)

    def iv(self):
        return chr(0) * 16


def key_gen():
    rnd_raw = Random.new().read(32)
    return b64encode(rnd_raw)


def session_key_gen():
    hsh = md5()
    hsh.update(str(randint(-9999999, 9999999)).encode('utf-8'))
    return b64encode(hsh.hexdigest().encode('utf-8')).decode('utf-8')


def passwd_encode(passwd, string):
    key = md5(passwd).hexdigest()
    enc = AESCipher(key).encrypt(string)
    return enc


def passwd_decode(passwd, string):
    key = md5(passwd).hexdigest()
    dec = AESCipher(key).decrypt(string)
    return dec


# it isn't powerfull encryption algoritm
def crypt(string, hash):
    j = 0
    res = ''
    for i in string:
        res += chr(ord(i)+int(hash[j]))
        j = j+1 if j < len(hash) - 1 else 0
    return res


def traffic_crypt(data):
    '''
    s=b64encode(data.encode('utf-8')).decode('utf-8')
    hsh=''.join([str(randint(1,5)),str(randint(1,5)),str(randint(1,5)),str(randint(1,5)),str(randint(1,5)),str(randint(1,5)),str(randint(1,5))])
    crpt=crypt(s,hsh)
    s=b64encode(b64encode(hsh.encode('utf-8'))).decode('utf-8')
    s+=crpt
    '''
    return b64encode(data)


def traffic_decrypt(data):
    '''
    hsh = b64decode(b64decode(data[:16].encode('utf-8'))).decode('utf-8')
    j = 0
    res = ''
    string = b64decode(data[16:].encode('utf-8')).decode('utf-8')
    for i in string:
        res+=chr(ord(i)-int(hsh[j]))
        j=j+1 if j < len(hsh)-1 else 0
    return b64decode(res.encode('utf-8')).decode('utf-8')
    '''
    return b64decode(data)
