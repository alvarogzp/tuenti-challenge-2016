#!/usr/bin/env python3

import socket
import re
import collections

HANGMAN_ADDRESS = ("52.49.91.111", 9988)
RECV_BUFFER = 4096

WORDS = open("words.txt").read().splitlines()


class WordList:
    def __init__(self, words):
        self.words = words

    def discard_not_matching_length(self, length):
        self.words = [word for word in self.words if len(word) == length]

    def discard_containing(self, letter):
        self.words = [word for word in self.words if letter not in word]

    def discard_not_matching(self, pattern):
        self.words = [word for word in self.words if pattern.match(word)]

    def get_most_frequent_letters(self):
        all_words_joined = "".join(self.words)
        frequency_dict = collections.Counter(all_words_joined)
        sorted_frequency_items = sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True)
        return [letter for letter, frequency in sorted_frequency_items]


class Game:
    def __init__(self, connection, words):
        self.connection = connection
        self.words = words
        self.used_letters = []
        self.word_hint = None

    def play(self):
        self.word_hint = self.get_word_hint()
        self.words.discard_not_matching_length(len(self.word_hint))
        while not self.is_game_completed():
            letter = self.choose_next_letter_to_select()
            self.select_letter(letter)

    def get_word_hint(self):
        return self.connection.get_word_line()

    def select_letter(self, letter):
        self.used_letters.append(letter)
        self.connection.send_letter(letter)
        self.word_hint = self.get_word_hint()
        if letter not in self.word_hint:
            self.words.discard_containing(letter)
        else:
            self.discard_words_not_matching(self.word_hint)

    def discard_words_not_matching(self, word_line):
        any_letter_except_used_ones = "[^" + "".join(self.used_letters) + "]"
        pattern = re.compile("^" + word_line.replace("_", any_letter_except_used_ones) + "$")
        self.words.discard_not_matching(pattern)

    def choose_next_letter_to_select(self):
        for letter in self.words.get_most_frequent_letters():
            if letter not in self.used_letters:
                return letter

    def is_game_completed(self):
        return self.word_hint.find("_") == -1


class GameFailedException(Exception): pass


class ChallengePassedNotification(Exception): pass


class GameSession:
    def __init__(self):
        self.connection = Connection(HANGMAN_ADDRESS)

    def run(self):
        self.connection.discard_received()

        while True:
            self.connection.press_enter()
            game = Game(self.connection, WordList(WORDS))
            game.play()


class Challenge:
    def run(self):
        session = GameSession()
        try:
            session.run()
        except GameFailedException:
            self.run()
        except ChallengePassedNotification:
            pass


class Connection:
    def __init__(self, address):
        self.socket = socket.create_connection(address)

    def get_word_line(self):
        received = self.receive_string()
        if "GAME OVER" in received:
            raise GameFailedException()
        if "Congratulations, Master!" in received:
            raise ChallengePassedNotification()
        return received.splitlines()[-3].replace(" ", "")

    def discard_received(self):
        self.receive_string()

    def press_enter(self):
        self.send("\n")

    def send_letter(self, letter):
        self.send(letter)

    def send(self, string):
        self.dump(string)
        self.socket.send(string.encode("utf8"))

    def receive_string(self):
        received = self.socket.recv(RECV_BUFFER).decode("utf8")
        self.dump(received)
        return received

    def dump(self, string):
        print(string, end="")


Challenge().run()
