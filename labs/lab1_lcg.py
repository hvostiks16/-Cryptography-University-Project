import math
import random

class LCGCore:
    def __init__(self):
        self.m = 2**30 - 1
        self.a = 17**3
        self.c = 10946
        self.x0 = 29

    def lcg(self, n):
        sequence = []
        x = self.x0
        for _ in range(n):
            x = (self.a * x + self.c) % self.m
            sequence.append(x)
        return sequence

    @staticmethod
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcg_period(self): 
        x = (self.a * self.x0 + self.c) % self.m 
        first = x
        count = 0
        while True: 
            x = (self.a * x + self.c) % self.m 
            count += 1 
            if x == first:
                break
        return count

    def estimate_pi_lcg(self, n):
        coprime_count = 0
        x = self.x0
        for _ in range(n):
            x = (self.a * x + self.c) % self.m 
            rand_x = x 
            x = (self.a * x + self.c) % self.m 
            rand_y = x
            if self.gcd(rand_x, rand_y) == 1: 
                coprime_count += 1
        p = coprime_count / n
        if p == 0: 
            return None 
        return math.sqrt(6 / p)

    def estimate_pi_system(self, n):
        coprime_count = 0
        for _ in range(n):
            rand_x = random.randint(1, self.m)
            rand_y = random.randint(1, self.m)
            if self.gcd(rand_x, rand_y) == 1: 
                coprime_count += 1
        p = coprime_count / n
        if p == 0: 
            return None 
        return math.sqrt(6 / p)