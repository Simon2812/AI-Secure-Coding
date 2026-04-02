from collections import defaultdict
from functools import cmp_to_key


class Row:
    def __init__(self, data):
        self._data = dict(data)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value

    def as_dict(self):
        return dict(self._data)


class Dataset:
    def __init__(self, rows):
        self._rows = [Row(r) for r in rows]

    def scan(self):
        for r in self._rows:
            yield r


class Expression:
    def __init__(self, func):
        self._func = func

    def eval(self, row):
        return self._func(row)


def field(name):
    return Expression(lambda r: r.get(name))


def literal(value):
    return Expression(lambda r: value)


def eq(a, b):
    return Expression(lambda r: a.eval(r) == b.eval(r))


def gt(a, b):
    return Expression(lambda r: a.eval(r) > b.eval(r))


def add(a, b):
    return Expression(lambda r: a.eval(r) + b.eval(r))


def mul(a, b):
    return Expression(lambda r: a.eval(r) * b.eval(r))


class Operator:
    def __iter__(self):
        return self.run()

    def run(self):
        raise NotImplementedError()


class Scan(Operator):
    def __init__(self, dataset):
        self._dataset = dataset

    def run(self):
        yield from self._dataset.scan()


class Filter(Operator):
    def __init__(self, source, predicate):
        self._source = source
        self._predicate = predicate

    def run(self):
        for row in self._source:
            if self._predicate.eval(row):
                yield row


class Project(Operator):
    def __init__(self, source, mapping):
        self._source = source
        self._mapping = mapping  # name -> Expression

    def run(self):
        for row in self._source:
            new_row = Row({})
            for key, expr in self._mapping.items():
                new_row.set(key, expr.eval(row))
            yield new_row


class Sort(Operator):
    def __init__(self, source, keys):
        self._source = source
        self._keys = keys  # [(Expression, asc_bool)]

    def run(self):
        rows = list(self._source)

        def compare(a, b):
            for expr, asc in self._keys:
                va = expr.eval(a)
                vb = expr.eval(b)

                if va < vb:
                    return -1 if asc else 1
                if va > vb:
                    return 1 if asc else -1
            return 0

        rows.sort(key=cmp_to_key(compare))
        for r in rows:
            yield r


class AggregateFunction:
    def step(self, value):
        raise NotImplementedError()

    def finalize(self):
        raise NotImplementedError()


class Sum(AggregateFunction):
    def __init__(self):
        self._total = 0

    def step(self, value):
        self._total += value

    def finalize(self):
        return self._total


class Count(AggregateFunction):
    def __init__(self):
        self._count = 0

    def step(self, value):
        self._count += 1

    def finalize(self):
        return self._count


class Avg(AggregateFunction):
    def __init__(self):
        self._total = 0
        self._count = 0

    def step(self, value):
        self._total += value
        self._count += 1

    def finalize(self):
        if self._count == 0:
            return 0
        return self._total / self._count


class GroupBy(Operator):
    def __init__(self, source, keys, aggregates):
        self._source = source
        self._keys = keys  # [(name, Expression)]
        self._aggregates = aggregates  # name -> (Expression, AggregateFunction factory)

    def run(self):
        buckets = {}

        for row in self._source:
            key_values = tuple(expr.eval(row) for _, expr in self._keys)

            if key_values not in buckets:
                buckets[key_values] = {
                    "aggs": {
                        name: factory()
                        for name, (_, factory) in self._aggregates.items()
                    }
                }

            bucket = buckets[key_values]

            for name, (expr, _) in self._aggregates.items():
                value = expr.eval(row)
                bucket["aggs"][name].step(value)

        for key_values, data in buckets.items():
            new_row = Row({})

            for (name, _), value in zip(self._keys, key_values):
                new_row.set(name, value)

            for name, agg in data["aggs"].items():
                new_row.set(name, agg.finalize())

            yield new_row


class Limit(Operator):
    def __init__(self, source, count):
        self._source = source
        self._count = count

    def run(self):
        i = 0
        for row in self._source:
            if i >= self._count:
                break
            yield row
            i += 1


class Planner:
    def __init__(self):
        self._steps = []

    def scan(self, dataset):
        op = Scan(dataset)
        self._steps.append(op)
        return op

    def filter(self, source, predicate):
        op = Filter(source, predicate)
        self._steps.append(op)
        return op

    def project(self, source, mapping):
        op = Project(source, mapping)
        self._steps.append(op)
        return op

    def group_by(self, source, keys, aggregates):
        op = GroupBy(source, keys, aggregates)
        self._steps.append(op)
        return op

    def sort(self, source, keys):
        op = Sort(source, keys)
        self._steps.append(op)
        return op

    def limit(self, source, count):
        op = Limit(source, count)
        self._steps.append(op)
        return op

    def explain(self):
        plan = []

        for step in self._steps:
            plan.append(step.__class__.__name__)

        return tuple(plan)


class ResultSet:
    def __init__(self, operator):
        self._operator = operator

    def collect(self):
        return [row.as_dict() for row in self._operator]

    def first(self):
        for row in self._operator:
            return row.as_dict()
        return None

    def to_columns(self):
        columns = defaultdict(list)

        for row in self._operator:
            for k, v in row.as_dict().items():
                columns[k].append(v)

        return dict(columns)


class Pipeline:
    def __init__(self, dataset):
        self._planner = Planner()
        self._current = self._planner.scan(dataset)

    def where(self, predicate):
        self._current = self._planner.filter(self._current, predicate)
        return self

    def select(self, mapping):
        self._current = self._planner.project(self._current, mapping)
        return self

    def group(self, keys, aggregates):
        self._current = self._planner.group_by(self._current, keys, aggregates)
        return self

    def order(self, keys):
        self._current = self._planner.sort(self._current, keys)
        return self

    def take(self, n):
        self._current = self._planner.limit(self._current, n)
        return self

    def execute(self):
        return ResultSet(self._current)

    def explain(self):
        return self._planner.explain()
