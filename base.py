from abc import ABC, abstractmethod

class aoc_solver(ABC):
    @abstractmethod
    def solve_a(self, input):
        pass
    @abstractmethod
    def solve_b(self, input):
        pass
