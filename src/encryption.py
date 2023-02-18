from os import system, name as os_name
from base64 import b64decode
from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class AESCipher:
    def __init__(self, pwd: str, salt: bytes):
        # self.key = md5(pwd.encode('utf8')).digest()
        self.key = PBKDF2(pwd, salt, dkLen=16)

    def encrypt(self, data: str):
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(pad(data.encode('utf-8'), AES.block_size)))

    def decrypt(self, data: bytes):
        raw = b64decode(data)
        cipher = AES.new(self.key, AES.MODE_CBC, raw[:AES.block_size])
        return unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size)


if __name__ == "__main__":
    system("cls" if "nt" in os_name else "clear")

    print("encrypt")
    namak = get_random_bytes(32)
    enc = AESCipher(input("password "), salt=namak)
    msg = input("message> ")


    system("cls" if "nt" in os_name else "clear")

    encrypted = enc.encrypt(msg)
    print("decrypt")
    denc = AESCipher(input("password "), namak)
    decrypted = enc.decrypt(encrypted)
    print("message>", decrypted.decode("utf-8"))
