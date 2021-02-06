from Crypto.Cipher import DES
DESIV={ 0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF}
def DESEnCode(pToEncrypt):

  generator = DES.new(DESIV, DES.MODE_ECB)
  # 非8整数倍明文补位
  pad = 8 - len(pToEncrypt) % 8
  pad_str = ""
  for i in range(pad):
    pad_str = pad_str + chr(pad)
  # 加密
  encrypted = generator.encrypt(pToEncrypt + pad_str)
  return encrypted
def DESDeCode(pToDecrypt):

  key = '1234A#CD'
  # ECB方式
  generator = DES.new(key, DES.MODE_ECB)
  # 解码
  result = generator.decrypt(pToDecrypt)
  # 替换非空格字符(诡异的串)
  result = result.strip("�����")
  result = result.strip("������")
  return result
