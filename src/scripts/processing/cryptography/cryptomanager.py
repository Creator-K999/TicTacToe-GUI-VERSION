from random import randint


class CryptoManager:

    __KEY = randint(0, 255)
    __CONSTANT = 100

    @classmethod
    def encrypt(cls, message):
        print(cls.__KEY)
        return [~(cls.__KEY ^ ord(letter)) + cls.__CONSTANT for letter in message]

    @classmethod
    def decrypt(cls, message):
        return "".join(chr(~(letter - cls.__CONSTANT) ^ cls.__KEY) for letter in message)
