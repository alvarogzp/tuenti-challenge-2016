#!/usr/bin/env python3

import socket

CHALLENGE_ADDRESS = ("52.49.91.111", 1986)
RECV_BUFFER = 4096

DIRECTION_LEFT = 'l'
DIRECTION_RIGHT = 'r'
DIRECTION_UP = 'u'
DIRECTION_DOWN = 'd'

OPPOSITE_DIRECTION = {
    DIRECTION_LEFT: DIRECTION_RIGHT,
    DIRECTION_RIGHT: DIRECTION_LEFT,
    DIRECTION_UP: DIRECTION_DOWN,
    DIRECTION_DOWN: DIRECTION_UP,
}

MAP_WALL = '#'
MAP_EMPTY = ' '
MAP_ME = 'x'


class Challenge:
    def __init__(self):
        self.connection = Connection()
        self.current_coordinates = (0, 0)
        self.visited_coordinates = []
        self.labyrinth = {}

    def run(self):
        self.step(None)
        self.print_labyrinth()

    def step(self, previous_direction):
        labyrinth = self.connection.get_labyrinth_received()
        self.save_labyrinth(labyrinth)
        available_directions = self.get_available_directions(labyrinth)
        for next_direction in available_directions:
            if not self.is_visited(next_direction):
                self.go_to(next_direction)
        # no more directions
        if previous_direction is not None:
            self.go_back(previous_direction)

    def go_to(self, direction):
        self.connection.go_to(direction)
        self.visited_coordinates.append(self.get_next_coordinates(direction))
        self.update_current_coordinates(direction)
        self.step(direction)

    def go_back(self, direction):
        opposite_direction = OPPOSITE_DIRECTION[direction]
        self.connection.go_to(opposite_direction)
        self.update_current_coordinates(opposite_direction)
        # discard as we already know the position
        self.connection.get_labyrinth_received()

    def get_available_directions(self, labyrinth):
        available_directions = []
        line, column = self.find_me(labyrinth)
        if column > 0 and labyrinth[line][column-1] != MAP_WALL:
            available_directions.append(DIRECTION_LEFT)
        if column+1 < len(labyrinth[line]) and labyrinth[line][column+1] != MAP_WALL:
            available_directions.append(DIRECTION_RIGHT)
        if line > 0 and labyrinth[line-1][column] != MAP_WALL:
            available_directions.append(DIRECTION_UP)
        if line+1 < len(labyrinth) and labyrinth[line+1][column] != MAP_WALL:
            available_directions.append(DIRECTION_DOWN)
        return available_directions

    def find_me(self, labyrinth):
        for line_number in range(len(labyrinth)):
            me = labyrinth[line_number].find(MAP_ME)
            if me != -1:  # me found!
                return line_number, me
        raise Exception("me not found")

    def update_current_coordinates(self, direction):
        self.current_coordinates = self.get_next_coordinates(direction)

    def get_next_coordinates(self, direction):
        line_coordinate = self.current_coordinates[0]
        column_coordinate = self.current_coordinates[1]
        if direction == DIRECTION_UP:
            line_coordinate -= 1
        if direction == DIRECTION_DOWN:
            line_coordinate += 1
        if direction == DIRECTION_LEFT:
            column_coordinate -= 1
        if direction == DIRECTION_RIGHT:
            column_coordinate += 1
        return line_coordinate, column_coordinate

    def is_visited(self, direction):
        next_coordinates = self.get_next_coordinates(direction)
        return next_coordinates in self.visited_coordinates

    def save_labyrinth(self, labyrinth):
        me_line, me_column = self.find_me(labyrinth)
        for line_index in range(len(labyrinth)):
            line = labyrinth[line_index]
            for column_index in range(len(line)):
                character = line[column_index]
                if character == MAP_ME:
                    character = MAP_EMPTY
                character_line = self.current_coordinates[0] + line_index - me_line
                character_column = self.current_coordinates[1] + column_index - me_column
                self.labyrinth[(character_line, character_column)] = character

    def print_labyrinth(self):
        last_line = 0
        for position in sorted(self.labyrinth.keys()):
            if position[0] != last_line:
                last_line = position[0]
                print()
            print(self.labyrinth[position], end="")
        print()


class Connection:
    def __init__(self):
        self.socket = socket.create_connection(CHALLENGE_ADDRESS)

    def get_labyrinth_received(self):
        return self.receive().splitlines()

    def go_to(self, direction):
        self.send(direction + "\n")

    def send(self, string):
        self.dump(string)
        self.socket.send(string.encode("utf8"))

    def receive(self):
        received = self.socket.recv(RECV_BUFFER).decode("utf8")
        self.dump(received)
        return received

    def dump(self, string):
        print(string, end="")


Challenge().run()
