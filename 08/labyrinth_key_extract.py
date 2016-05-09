#!/usr/bin/env python3

labyrinth = open("labyrinth.txt").read().splitlines()
labyrinth_lines = len(labyrinth)
labyrinth_columns = len(labyrinth[0])

NO_KEY_CHARACTERS = [' ', '#', '>']

key_positions = {}

for line_index in range(labyrinth_lines):
    line = labyrinth[line_index]
    for column_index in range(labyrinth_columns):
        character = line[column_index]
        if character not in NO_KEY_CHARACTERS:
            key_positions[(line_index, column_index)] = character

def key_sorting(key):
    line = key[0]
    column = key[1]
    if line == 1:  # first upper line characters
        return column
    if column == labyrinth_columns - 2:  # then last column characters
        return labyrinth_columns + line
    if line == labyrinth_lines - 2:  # next last line characters reversed
        return labyrinth_columns + labyrinth_lines + labyrinth_columns - column
    if column == 1:  # and finally first column characters reversed
        return labyrinth_columns + labyrinth_lines + labyrinth_columns + labyrinth_lines - line

for position in sorted(key_positions, key=key_sorting):
    print(key_positions[position], end="")
print()
