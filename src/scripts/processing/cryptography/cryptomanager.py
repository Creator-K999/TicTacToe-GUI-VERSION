from random import randint


class CryptoManager:

    __CONSTANT = 100

    @classmethod
    def get_new_key(cls):
        return randint(0, 255)

    @classmethod
    def encrypt(cls, message, key):
        return *(str(~(key ^ ord(letter)) + cls.__CONSTANT) for letter in message), f"{key}"

    @classmethod
    def decrypt(cls, message, key):
        return "".join(chr(~(letter - cls.__CONSTANT) ^ key) for letter in message)
