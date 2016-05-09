#!/usr/bin/env python3

import sys
import yaml # pip3 install pyyaml


# dicts have no ordering in python, so we define here the execution order for
# actions to avoid tape move before write
INSTRUCTION_ACTIONS_ORDER = ["write", "move", "state"]


class Instruction:
    def __init__(self, actions):
        self.actions = actions

    def perform_actions(self, program, tape):
        for action_name, action_value in self.actions:
            action_function = eval("self.perform_action_" + action_name)
            action_function(program, tape, action_value)

    def perform_action_state(self, program, tape, new_state):
        program.current_state = new_state

    def perform_action_move(self, program, tape, direction):
        tape_move_function = eval("tape.move_" + direction)
        tape_move_function()

    def perform_action_write(self, program, tape, new_value):
        tape.write_value(new_value)


class Program:
    def __init__(self, states):
        self.states = states
        self.reset()

    def reset(self):
        self.current_state = "start"

    def execute(self, tape):
        while self.current_state != "end":
            code = tape.read_value()
            self.execute_instruction(tape, code)

    def execute_instruction(self, tape, code):
        instruction = self.states[self.current_state][code]
        instruction.perform_actions(self, tape)


class Tape:
    def __init__(self, initial_tape_data):
        self.tape_data = list(initial_tape_data)
        self.current_position = 0

    def read_value(self):
        if self.current_position >= len(self.tape_data):
            return " "
        return self.tape_data[self.current_position]

    def write_value(self, value):
        if self.current_position >= len(self.tape_data):
            self.tape_data.append(value)
        else:
            self.tape_data[self.current_position] = value

    def move_right(self):
        self.current_position += 1

    def move_left(self):
        self.current_position -= 1

    def get_full_data(self):
        return "".join(self.tape_data)


config = yaml.load(sys.stdin)
states = config["code"]
tapes = config["tapes"]

new_states = dict()
for state_name, state_content in states.items():
    new_state_content = dict()
    for instruction_code, instruction_actions in state_content.items():
        sorted_instructions_actions = sorted(instruction_actions.items(), key=lambda x: INSTRUCTION_ACTIONS_ORDER.index(x[0]))
        instruction = Instruction(sorted_instructions_actions)
        new_state_content[instruction_code] = instruction
    new_states[state_name] = new_state_content

program = Program(new_states)


for tape_number, tape_data in tapes.items():
    tape = Tape(tape_data)
    program.reset()
    program.execute(tape)
    final_state = tape.get_full_data()
    print("Tape #%s: %s" % (tape_number, final_state))
