import csv


def func(dataclass):
    def to_csv(self, delimeter = ','):
        return delimeter.join(str(getattr(self, k)) for k in self.__annotations__)

    dataclass.to_csv = to_csv

    def _from_csv_single(cls, csv):
        args = (t(d) for d, t in zip(csv, cls.__annotations__.values()))
        return cls(*args)

    dataclass._from_csv_single = classmethod(_from_csv_single)

    def from_csv(cls, file, **kwargs):
        with open(file, newline = '') as csvfile:
            spamreader = csv.reader(csvfile, **kwargs)
            for row in spamreader:
                yield cls._from_csv_single(row)

    dataclass.from_csv = classmethod(from_csv)

    return dataclass
