#!/usr/bin/env python3


class TrainingSession:
    def __init__(self, moves):
        self.moves = tuple(moves)

    def is_move_at(self, move, index):
        if index >= len(self.moves) or index < 0:
            return False
        return self.moves[index] == move

    def next_move_or_none(self, move, starting_at):
        try:
            return self.moves.index(move, starting_at)
        except ValueError:
            return None


class Combo:
    def __init__(self, moves, last_move, invalidated_if_preceded_by):
        self.moves = tuple(moves)
        self.last_move = last_move
        self.invalidated_if_preceded_by = tuple(invalidated_if_preceded_by)

    def get_combos_for(self, training_session):
        number_of_combos = 0
        current_index = 0
        while current_index is not None:
            current_index = training_session.next_move_or_none(self.moves[0], current_index)
            if current_index is not None:
                if self.is_combo_at(training_session, current_index):
                    number_of_combos += 1
                current_index += 1  # search for next combo
        return number_of_combos

    def is_combo_at(self, training_session, training_session_index):
        # check precedent moves are not forbidden
        if self.are_precedent_moves_forbidden(training_session, training_session_index):
            return False
        # start on second move, as first one has already been checked by caller
        training_session_index += 1
        move_index = 1
        while move_index < len(self.moves):
            if not training_session.is_move_at(self.moves[move_index], training_session_index):
                return False
            training_session_index += 1
            move_index += 1
        # all moves matched, check last move doesn't match
        if training_session.is_move_at(self.last_move, training_session_index):
            return False
        return True

    def are_precedent_moves_forbidden(self, training_session, training_session_index):
        if len(self.invalidated_if_preceded_by) == 0:
            return False  # no forbidden precedents
        training_session_index -= 1
        precedent_index = len(self.invalidated_if_preceded_by) - 1
        while precedent_index >= 0:
            if not training_session.is_move_at(self.invalidated_if_preceded_by[precedent_index], training_session_index):
                return False
            training_session_index -= 1
            precedent_index -= 1
        return True


COMBOS = [
    Combo(["L", "LD", "D", "RD", "R"], "P", []),
    Combo(           ["D", "RD", "R"], "P", ["L", "LD"]),
    Combo(           ["R", "D", "RD"], "P", []),
    Combo(           ["D", "LD", "L"], "K", ["R", "RD"]),
    Combo(["R", "RD", "D", "LD", "L"], "K", [])
]


number_of_cases = int(input())
for case_number in range(number_of_cases):
    training_session = TrainingSession(input().split("-"))
    combos_without_last_move = sum([combo.get_combos_for(training_session) for combo in COMBOS])
    print("Case #%s: %s" % (case_number + 1, combos_without_last_move))
