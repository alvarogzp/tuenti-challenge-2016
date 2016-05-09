#!/usr/bin/env python3

CACHED_EXP = {}


def get_exp(e):
    if e not in CACHED_EXP:
        exp = 10 ** e
        CACHED_EXP[e] = exp
    else:
        exp = CACHED_EXP[e]
    return exp


class ImmiscibleNumberGenerator:
    def __init__(self):
        self.current_number = 0
        self.number_of_digits = 0
        self.current_one_digit = 1

    def immiscible_numbers(self):
        while True:
            if self.all_are_ones():
                self.add_another_digit()
            else:
                self.put_another_one()
            yield self.current_number

    def all_are_ones(self):
        return self.current_one_digit == 0

    def add_another_digit(self):
        self.number_of_digits += 1
        self.current_one_digit = self.number_of_digits
        self.current_number = get_exp(self.number_of_digits)

    def put_another_one(self):
        self.current_one_digit -= 1
        self.current_number += get_exp(self.current_one_digit)


class ImmiscibleMultipleFinder:
    def __init__(self, number):
        self.number = number
        self.immiscible_numbers = ImmiscibleNumberGenerator()
        self.multiple = 0
        self.number_of_ones = 0
        self.number_of_zeros = 0

    def find(self):
        self.multiple = self.calculate_immiscible_multiple()
        self.calculate_number_of_ones_and_zeros()

    def calculate_immiscible_multiple(self):
        for immiscible_number in self.immiscible_numbers.immiscible_numbers():
            if immiscible_number % self.number == 0:
                return immiscible_number

    def calculate_number_of_ones_and_zeros(self):
        multiple_str = str(self.multiple)
        self.number_of_ones = multiple_str.find("0")
        if self.number_of_ones == -1:
            self.number_of_ones = len(multiple_str)
            self.number_of_zeros = 0
        else:
            self.number_of_zeros = len(multiple_str) - self.number_of_ones


number_of_cases = int(input())
for case_number in range(number_of_cases):
    finder = ImmiscibleMultipleFinder(int(input()))
    finder.find()
    print("Case #%s: %s %s" % (case_number + 1, finder.number_of_ones, finder.number_of_zeros))
