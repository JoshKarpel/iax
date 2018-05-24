import datetime

import iax


@iax.iax()
class Foo:
    a: int
    b: str


print(Foo)

f = Foo(a = 1, b = 'hi')
f2 = Foo(a = 2, b = 'lo')
print(f)

# for k, v in Foo.__dict__.items():
#     print(k, v)

csv = Foo.to_csv(file = 'csv.csv', items = [f, f2], delimiter = ',', write_header = True)
print(list(Foo.from_csv('csv.csv', delimiter = ',', has_header = True)))

json = Foo.to_json(file = 'json.json', items = [f, f2], indent = 4)
print(list(Foo.from_json('json.json')))
print(type(f.a))
