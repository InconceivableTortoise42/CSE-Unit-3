from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y