#!/usr/bin/env python3

def get_min_number_of_tables_for(number_of_persons):
    if number_of_persons == 0:
        return 0
    number_of_tables = 1
    persons_with_seat = 4 # one table sits 4 persons
    while persons_with_seat < number_of_persons:
        number_of_tables += 1
        persons_with_seat += 2 # for each new table, 2 more persons sit
    return number_of_tables

number_of_cases = int(input())

for case_number in range(number_of_cases):
    persons = int(input())
    print("Case #" + str(case_number + 1) + ": " + str(get_min_number_of_tables_for(persons)))
