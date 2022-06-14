from random import randint


class CryptoManager:

    __KEY = randint(0, 255)
    __CONSTANT = 100

    @classmethod
    def get_key(cls):
        return cls.__KEY

    @classmethod
    def encrypt(cls, message):
        print(cls.__KEY)
        return [str(~(cls.__KEY ^ ord(letter)) + cls.__CONSTANT) for letter in message]

    @classmethod
    def decrypt(cls, message, key=None):
        if key is None:
            return "".join(chr(~(letter - cls.__CONSTANT) ^ cls.__KEY) for letter in message)

        return "".join(chr(~(letter - cls.__CONSTANT) ^ key) for letter in message)
