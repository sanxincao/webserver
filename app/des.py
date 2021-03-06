import binascii
import base64
import pyDes
#phone		Value	"jYMsUrZkT9vrfOdxUnl25w=="	string
#password		Value	"FZz3LAvSqBjRKk7RbJ2cAQ=="	string

class DES:
    #IV必须是 8 字节长度的十六进制数
    iv = '1234567812345678'
    #key加密密钥长度，24字节
    key = '12345678'
    def __init__(self, iv, key):
        self.iv = iv
        self.key = key
    def encrypt(self, data):
        k = pyDes.triple_des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        d = k.encrypt(data)
        d = base64.encodestring(d)
        return d
    def decrypt(self, data):
        k = pyDes.triple_des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        data = base64.decodestring(data)
        d = k.decrypt(data)
        return d
if __name__ == '__main__':

    des = DES('12345678','1234567812345678')

    decryptdata = des.decrypt(b'jYMsUrZkT9vrfOdxUnl25w==')
    print(decryptdata)