import numpy as np
import random


class Bacterium:
    def __init__(self, mapping, x_, y_, energy, mutation_probability):
        self.m = mapping
        self.state = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
        self.x = x_
        self.y = y_
        self.antibiotics = 0
        self.resistance = [0, 0]  # resistance = self.resistance[0] - 10 * self.resistance[1]
        self.energy = energy
        self.mutation_probability = mutation_probability

    def get_action(self):  # actions available: move, reproduce
        self.energy -= 1 + abs(self.antibiotics - (self.resistance[0] - 10 * self.resistance[1]))
        self.state[4] = self.energy / self.reproduction_energy()
        product = [0] * len(self.state)
        for i in range(len(self.state)):
            for j in range(len(self.m[0])):
                product[j] += self.state[i] * self.m[i][j]
        return product

    def move(self, new_pos):
        self.x, self.y = new_pos

    def reproduce(self):
        rep_energy = self.reproduction_energy()
        self.state[4] -= rep_energy
        child_mapping = np.copy(self.m)
        # print(self.m)

        if random.random() <= self.mutation_probability / 10:
            for i in range(int(abs(np.random.normal(0, self.mutation_probability)))):
                change = np.random.normal(0, 0.1)
                # print(change)
                child_mapping[random.randint(0, len(child_mapping) - 1)][
                    random.randint(0, len(child_mapping[0]) - 1)] += change
                child_mapping[random.randint(0, len(child_mapping) - 1)][
                    random.randint(0, len(child_mapping[0]) - 1)] -= change

        # print(child_mapping)
        child = Bacterium(child_mapping,
                          self.x, self.y,
                          rep_energy - 1,
                          max(0.05, min(1, self.mutation_probability + np.random.normal(0, self.mutation_probability, 1))))
        child.set_resistance(self.randomize_resistance())
        return child

    def input(self, inp):
        for i in range(len(inp)):
            self.state[i] = inp[i]

    def change_energy(self, new_energy):
        self.energy = new_energy

    def get_energy(self):
        return self.energy

    def reproduction_energy(self):
        return self.resistance[0] + 5

    def get_position(self):
        return self.x, self.y

    def introduce_antibiotic(self, antibiotic_level):
        self.antibiotics = antibiotic_level

    def set_resistance(self, new_resistance):
        self.resistance = new_resistance

    def randomize_resistance(self):
        return self.resistance[0] + np.random.normal(0, self.mutation_probability), \
               self.resistance[1] + np.random.normal(0, self.mutation_probability)
