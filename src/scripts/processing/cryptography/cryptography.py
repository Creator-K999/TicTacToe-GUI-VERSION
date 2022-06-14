from os import urandom


class Cryptography:

    __KEY = int(urandom(1).decode("utf-8"))
    __CONSTANT = 100

    @classmethod
    def encrypt(cls, message):
        return "".join(~(cls.__KEY ^ ~ord(letter)) - cls.__CONSTANT for letter in message)

    @classmethod
    def decrypt(cls, message):
        return "".join(~(ord(letter) - cls.__CONSTANT) ^ cls.__KEY for letter in message)
