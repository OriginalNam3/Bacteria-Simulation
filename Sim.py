import numpy as np
import random
import matplotlib
from Bacteria import Bacterium

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]


class Simulation:
    def __init__(self, height, width, bacterium_template, initial_size, food_per_frame, initial_mutation_rate):
        self.h = height
        self.w = width
        self.grid = np.zeros((width, height), dtype=np.int64)
        self.food_count = [[0] * width, [0] * height]
        self.pref = [[0] * width, [0] * height]
        for _ in range(int(height * width * 0.5)):
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            self.grid[x][y] += 1
            self.food_count[0][x] += 1
            self.food_count[1][y] += 1
        self.organisms = [Bacterium(bacterium_template, random.randint(0, width - 1), random.randint(0, height - 1), 50, initial_mutation_rate)
                      for _ in range(initial_size)]
        self.population = initial_size
        self.fpf = food_per_frame

    def simulate(self):
        t = 0
        while True:
            for i in range(self.fpf):
                x, y = random.randint(0, self.w - 1), random.randint(0, self.h - 1)
                self.grid[x][y] += 1
                self.food_count[0][x] += 1
                self.food_count[1][y] += 1
            # print(self.grid)
            self.pref[0][0], self.pref[1][0] = self.food_count[0][0], self.food_count[1][0]
            for i in range(1, self.w):
                self.pref[0][i] = self.pref[0][i-1] + self.food_count[0][i]
            for i in range(1, self.h):
                self.pref[1][i] = self.pref[1][i-1] + self.food_count[1][i]
            # print(self.pref)
            for bacterium in self.organisms:
                pos = list(bacterium.get_position())
                if 200 < t < 400:
                    bacterium.introduce_antibiotic(20)
                if t >= 400:
                    bacterium.introduce_antibiotic(0)
                bacterium.change_energy(bacterium.get_energy() + self.grid[pos[0]][pos[1]])
                self.food_count[0][pos[0]] -= self.grid[pos[0]][pos[1]]
                self.food_count[1][pos[1]] -= self.grid[pos[0]][pos[1]]
                self.grid[pos[0]][pos[1]] = 0
                senses = [(self.pref[0][min(self.w - 1, pos[0] + 5)] - self.pref[0][pos[0]])/self.pref[0][self.w-1],
                          (self.pref[1][min(self.h - 1, pos[1] + 5)] - self.pref[1][pos[1]])/self.pref[1][self.h-1],
                          (self.pref[0][max(0, pos[0] - 1)] - self.pref[0][max(0, pos[0] - 6)])/self.pref[1][self.w-1],
                          (self.pref[1][max(0, pos[1] - 1)] - self.pref[1][max(0, pos[1] - 6)])/self.pref[1][self.h-1]]
                # print(senses)
                bacterium.input(senses)
                action = bacterium.get_action()
                # print(action)
                # print(action)
                ind = 0
                mx = -1000000000
                for i in range(len(action)):
                    if action[i] > mx:
                        mx = action[i]
                        ind = i
                if ind < 4:
                    pos[0] = min(self.w - 1, max(0, pos[0] + dx[ind]))
                    pos[1] = min(self.h - 1, max(0, pos[1] + dy[ind]))
                    bacterium.move(pos)
                else:
                    if bacterium.get_energy() > bacterium.reproduction_energy():
                        self.population += 1
                        self.organisms.append(bacterium.reproduce())
                if bacterium.get_energy() <= 0:
                    self.population -= 1
                    self.organisms.remove(bacterium)

            print(len(self.organisms), t)
            t += 1
