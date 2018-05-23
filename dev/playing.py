import datetime

from dataclasses import dataclass

import iax


@iax.iax
@dataclass
class Foo:
    a: int
    b: str


print(Foo)

f = Foo(a = 1, b = 'hi')
f2 = Foo(a = 2, b = 'lo')
print(f)

# for k, v in Foo.__dict__.items():
#     print(k, v)

csv = f.to_csv(file = 'csv.csv', items = [f, f2], delimiter = ',', write_header = True)
print(list(Foo.from_csv('csv.csv', delimiter = ',', has_header = True)))
