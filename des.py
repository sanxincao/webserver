import binascii
import base64
import pyDes
#phone		Value	"jYMsUrZkT9vrfOdxUnl25w=="	string
#password		Value	"FZz3LAvSqBjRKk7RbJ2cAQ=="	string

class DES:
    #IV必须是 8 字节长度的十六进制数

    #key加密密钥长度，24字节

    #TODO 加密密钥暂时固定
    def __init__(self):
        self.iv = '12345678'
        self.key = '1234567812345678'
    def encrypt(self, data):
        k = pyDes.triple_des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        d = k.encrypt(data)
        d = base64.encodebytes(d)
        result=d.decode("utf-8")
        return result
    def decrypt(self, data):
        bdata=bytes(data, 'utf-8')
        k = pyDes.triple_des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        data = base64.decodebytes(bdata)
        d = k.decrypt(data)
        result=d.decode("utf-8")
        return result

#Ec9C/XMDbtAnQrOMF51g4w==
#Ec9C/XMDbtAnQrOMF51g4w==
#FZz3LAvSqBjRKk7RbJ2cAQ==
#FZz3LAvSqBjRKk7RbJ2cAQ==