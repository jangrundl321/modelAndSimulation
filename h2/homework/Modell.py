# implementation of exercise 2.2.2
# Modell.py contains specifications for DEVS models
# comment/TODO:
# - There should not be a issue with the model implementation

import random


class Region:

    def __init__(self, pos):
        self.type = "Region"
        self.name = "Region" + str(pos)
        self.pos = pos
        self.initial_state = "wood"
        self.current_state = self.initial_state

    def deltaInt(self):
        state = self.current_state
        self.current_state = {"wood": "wood",
                             "meadow": "wood",
                             "fire": "meadow"}[state]
        return self.current_state

    def deltaExt(self, elapsed_time, x):
        state = self.current_state
        if x == "MatchMessage" and random.random() < 0.01:
            self.current_state = "fire"
            return "fire"
        if x == "NeighborMatchMessage":
            if state == "wood" and random.random() < 0.10:
                self.current_state = "fire"
                return "fire"
            elif state == "meadow":
                self.current_state = "fire"
                return "fire"

        return state

    def ta(self):
        state = self.current_state
        return {"wood": 100000,
                "meadow": 5,
                "fire": 11}[state]

    def lambda_(self):
        state = self.current_state
        return {"wood": "EmptyMessage",
                "meadow": "NeighborMatchMessage",
                "fire": "EmptyMessage"}[state]


class Match:

    def __init__(self):
        self.type = "Match"
        self.name = "Match"
        self.initial_state = "fire"
        self.current_state = self.initial_state
        self.pos = (22, 22)

    def deltaInt(self):
        state = self.current_state
        self.current_state = {"fire": "fire"}[state]
        return self.current_state

    def deltaExt(self, elapsed_time, x):
        state = self.current_state
        self.current_state = state
        return self.current_state

    def ta(self):
        state = self.current_state
        return {"fire": 10}[state]

    def lambda_(self):
        return "MatchMessage"


class RootModel:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        root_model_grid = [[] for r in range(row)]

        self.match = Match()
        for r in range(row):
            for c in range(col):
                root_model_grid[r].append(Region((r, c)))
        self.root_model_grid = root_model_grid

    def get_neighbours(self, row, col):
        neighbours = []
        for x, y in (
                (row - 1, col), (row + 1, col), (row, col - 1),
                (row, col + 1), (row - 1, col - 1), (row - 1, col + 1),
                (row + 1, col - 1), (row + 1, col + 1)):
            if not ((0 <= x < len(self.root_model_grid)) and (0 <= y < len(self.root_model_grid[x]))):
                continue
            neighbours.append(self.root_model_grid[x][y])
        return neighbours

    def select(self, event_list):
        event_list = sorted(event_list, key=lambda x: (x[2], x[1]))
        return event_list

    def children_getting_input_by_child(self, child):
        if child.atomicDEVS.type == "Match":
            neighbours_as_names = []
            row = self.row
            col = self.col

            for r in range(row):
                for c in range(col):
                    neighbours_as_names.append(self.root_model_grid[r][c].name)

            return neighbours_as_names

        if child.atomicDEVS.type == "Region":
            (x, y) = child.atomicDEVS.pos
            neighbours_as_models = self.get_neighbours(x, y)
            neighbours_as_names = []

            for x in neighbours_as_models:
                neighbours_as_names.append(x.name)

            return neighbours_as_names
