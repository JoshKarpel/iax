import csv
import json

from dataclasses import dataclass, asdict


def ix(*args, **kwargs):
    def inner(dc):
        dc = dataclass(dc, **kwargs)

        dc.__iax__ = True

        ### CSV ###

        @attach(dc)
        def _to_csv_single(self, delimeter = ','):
            return delimeter.join(str(getattr(self, k)) for k in self.__annotations__)

        @attach(dc)
        @staticmethod
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

        def _to_csvs_helper(items, write_header = False, delimiter = ','):
            if write_header:
                yield delimiter.join(a for a in items[0].__annotations__)
            for item in items:
                yield delimiter.join(str(getattr(item, k)) for k in item.__annotations__)

        @attach(dc)
        @staticmethod
        def to_csvs(items, write_header = False, delimiter = ','):
            return '\n'.join(_to_csvs_helper(items, write_header = write_header, delimiter = delimiter))

        @attach(dc)
        @classmethod
        def _from_csv_single(cls, csv):
            args = (t(d) for d, t in zip(csv, cls.__annotations__.values()))
            return cls(*args)

        @attach(dc)
        @classmethod
        def from_csv(cls, file, has_header = False, **kwargs):
            with open(file, newline = '') as csvfile:
                reader = csv.reader(csvfile, **kwargs)
                if has_header:
                    next(reader)
                for row in reader:
                    yield cls._from_csv_single(row)

        ### JSON ###

        @attach(dc)
        @staticmethod
        def to_json(file, items, **kwargs):
            with open(file, mode = 'w') as jsonfile:
                json.dump(
                    [asdict(item) for item in items],
                    jsonfile,
                    **kwargs,
                )

        @attach(dc)
        @staticmethod
        def to_jsons(items, **kwargs):
            return json.dumps(
                [asdict(item) for item in items],
                **kwargs
            )

        @attach(dc)
        @classmethod
        def _from_json_single(cls, j):
            args = {}
            for key, value in j.items():
                t = cls.__annotations__[key]
                try:
                    v = t._from_json_single(value)
                except AttributeError:
                    v = t(value)
                args[key] = v

            return cls(**args)

        @attach(dc)
        @classmethod
        def from_json(cls, file):
            with open(file) as jsonfile:
                jsons = json.load(jsonfile)
                for j in jsons:
                    yield cls._from_json_single(j)

        @attach(dc)
        @classmethod
        def from_jsons(cls, jsons):
            js = json.loads(jsons)
            for j in js:
                yield cls._from_json_single(j)

        return dc

    # if called without parens, act directly on the first arg (the class)
    if len(args) == 1 and len(kwargs) == 0:
        return inner(args[0])

    return inner


def attach(cls):
    def attacher(func):
        try:
            name = func.__name__
        except AttributeError:
            name = func.__func__.__name__
        setattr(cls, name, func)

    return attacher
