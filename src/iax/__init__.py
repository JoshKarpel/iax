import csv
import json

from dataclasses import dataclass, asdict


def iax(**kwargs):
    def iax_inner(dc):
        dc = dataclass(dc, **kwargs)

        @attach(dc)
        def _to_csv_single(self, delimeter = ','):
            return delimeter.join(str(getattr(self, k)) for k in self.__annotations__)

        @attach(dc, staticmethod)
        def to_csv(file, items, write_header = False, **kwargs):
            with open(file, 'w', newline = '') as csvfile:
                writer = csv.writer(
                    csvfile,
                    **kwargs
                )
                if write_header:
                    writer.writerow(a for a in items[0].__annotations__)
                for item in items:
                    writer.writerow(getattr(item, k) for k in item.__annotations__)

        @attach(dc, classmethod)
        def _from_csv_single(cls, csv):
            args = (t(d) for d, t in zip(csv, cls.__annotations__.values()))
            return cls(*args)

        @attach(dc, classmethod)
        def from_csv(cls, file, has_header = False, **kwargs):
            with open(file, newline = '') as csvfile:
                reader = csv.reader(csvfile, **kwargs)
                if has_header:
                    next(reader)
                for row in reader:
                    yield cls._from_csv_single(row)

        @attach(dc, staticmethod)
        def to_json(file, items, **kwargs):
            with open(file, mode = 'w') as jsonfile:
                json.dump(
                    [asdict(item) for item in items],
                    jsonfile,
                    **kwargs,
                )

        @attach(dc, classmethod)
        def _from_json_single(cls, j):
            print(cls, j, cls.__annotations__)

            args = {}
            for key, value in j.items():
                t = cls.__annotations__[key]
                try:
                    v = t._from_json_single(value)
                except AttributeError:
                    v = t(value)
                args[key] = v

            return cls(**args)
            # return cls(**{k: cls.__annotations__[k](v) for k, v in j.items()})

        @attach(dc, classmethod)
        def from_json(cls, file):
            with open(file) as jsonfile:
                jsons = json.load(jsonfile)
                for j in jsons:
                    yield cls._from_json_single(j)

        return dc

    return iax_inner


def attach(cls, pre = None):
    def attacher(func):
        if pre is None:
            setattr(cls, func.__name__, func)
        else:
            setattr(cls, func.__name__, pre(func))

    return attacher
