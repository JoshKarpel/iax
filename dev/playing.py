from dataclasses import dataclass

import iax


@iax.func
@dataclass
class Foo:
    a: int
    b: str


print(Foo)

f = Foo(a = 1, b = 'hi')

print(f)

# for k, v in Foo.__dict__.items():
#     print(k, v)

csv = f.to_csv()
print(csv)
print(list(Foo.from_csv('csv.csv', delimiter = ',')))
