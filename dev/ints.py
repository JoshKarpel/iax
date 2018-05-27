import random

from ix import ix


@ix
class Ints:
    a: int
    b: int

    @classmethod
    def from_rand(cls):
        return cls(
            a = random.randint(-1000, 1000),
            b = random.randint(-1000, 1000),
        )


ints = [Ints.from_rand() for _ in range(10)]

for i in ints:
    print(i)

print()

print(Ints.to_csvs(ints, write_header = True))
