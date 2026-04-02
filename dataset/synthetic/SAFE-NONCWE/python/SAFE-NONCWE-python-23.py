from collections import defaultdict, deque


class VariableStore:
    def __init__(self):
        self._values = {}
        self._domains = {}
        self._dependents = defaultdict(set)

    def declare(self, name, domain):
        self._domains[name] = set(domain)
        self._values[name] = None

    def set(self, name, value):
        if name not in self._domains:
            raise ValueError(f"Unknown variable: {name}")

        if value not in self._domains[name]:
            raise ValueError(f"Invalid value {value} for {name}")

        self._values[name] = value

    def value(self, name):
        return self._values.get(name)

    def domain(self, name):
        return set(self._domains.get(name, set()))

    def restrict(self, name, allowed):
        current = self._domains[name]
        new_domain = current & set(allowed)

        if not new_domain:
            raise ValueError(f"Domain wiped out for {name}")

        if new_domain != current:
            self._domains[name] = new_domain
            return True

        return False

    def register_dependency(self, source, target):
        self._dependents[source].add(target)

    def dependents(self, name):
        return self._dependents.get(name, set())

    def unresolved(self):
        return [k for k, v in self._values.items() if v is None]


class Constraint:
    def __init__(self, name, variables, rule):
        self.name = name
        self.variables = tuple(variables)
        self.rule = rule

    def apply(self, store):
        return self.rule(store)


class ConstraintEngine:
    def __init__(self):
        self._constraints = []
        self._var_to_constraints = defaultdict(list)

    def add_constraint(self, constraint):
        self._constraints.append(constraint)

        for var in constraint.variables:
            self._var_to_constraints[var].append(constraint)

    def propagate(self, store):
        queue = deque(store._domains.keys())
        visited = set()

        while queue:
            var = queue.popleft()

            for constraint in self._var_to_constraints[var]:
                changed = constraint.apply(store)

                if changed:
                    for affected in constraint.variables:
                        if affected != var:
                            queue.append(affected)

            visited.add(var)

        return visited

    def validate(self, store):
        issues = []

        for constraint in self._constraints:
            if not constraint.rule(store):
                issues.append(constraint.name)

        return issues


def requires_if(store, a, a_val, b, allowed_b):
    if store.value(a) == a_val:
        return store.restrict(b, allowed_b)
    return False


def mutual_exclusion(store, a, b):
    va = store.value(a)
    vb = store.value(b)

    if va is not None and vb is not None:
        if va == vb:
            raise ValueError(f"{a} and {b} cannot share value {va}")
    return False


def conditional_domain(store, source, mapping, target):
    val = store.value(source)

    if val is None:
        return False

    allowed = mapping.get(val)
    if allowed is None:
        return False

    return store.restrict(target, allowed)


def sum_limit(store, variables, limit):
    total = 0

    for v in variables:
        val = store.value(v)
        if val is None:
            return False
        total += val

    if total > limit:
        raise ValueError("Sum constraint violated")

    return False


def build_engine():
    engine = ConstraintEngine()

    engine.add_constraint(Constraint(
        "region_requires_currency",
        ("region", "currency"),
        lambda s: requires_if(s, "region", "EU", "currency", {"EUR"})
    ))

    engine.add_constraint(Constraint(
        "plan_limits_storage",
        ("plan", "storage"),
        lambda s: conditional_domain(
            s,
            "plan",
            {
                "basic": {10, 20},
                "pro": {50, 100},
                "enterprise": {200, 500}
            },
            "storage"
        )
    ))

    engine.add_constraint(Constraint(
        "no_duplicate_modes",
        ("mode_a", "mode_b"),
        lambda s: mutual_exclusion(s, "mode_a", "mode_b")
    ))

    engine.add_constraint(Constraint(
        "resource_sum_limit",
        ("cpu", "memory"),
        lambda s: sum_limit(s, ("cpu", "memory"), 64)
    ))

    return engine


class ConflictAnalyzer:
    def __init__(self):
        self._history = []

    def record(self, constraint_name, variable):
        self._history.append((constraint_name, variable))

    def explain(self):
        explanation = defaultdict(list)

        for cname, var in self._history:
            explanation[cname].append(var)

        return dict(explanation)

    def most_problematic(self):
        counter = defaultdict(int)

        for cname, _ in self._history:
            counter[cname] += 1

        if not counter:
            return None

        return max(counter.items(), key=lambda x: x[1])[0]


class ScenarioRunner:
    def __init__(self, engine, store):
        self._engine = engine
        self._store = store
        self._conflicts = ConflictAnalyzer()

    def assign(self, name, value):
        try:
            self._store.set(name, value)
            self._engine.propagate(self._store)
        except ValueError:
            self._conflicts.record("assignment_failed", name)

    def auto_assign(self):
        progress = True

        while progress:
            progress = False

            for var in self._store.unresolved():
                domain = self._store.domain(var)

                if len(domain) == 1:
                    val = next(iter(domain))
                    try:
                        self._store.set(var, val)
                        self._engine.propagate(self._store)
                        progress = True
                    except ValueError:
                        self._conflicts.record("auto_assign_failed", var)

    def result(self):
        return dict(self._store._values)

    def conflicts(self):
        return self._conflicts.explain()

    def unstable_variables(self):
        unstable = []

        for var in self._store._domains:
            if len(self._store.domain(var)) > 3:
                unstable.append(var)

        return tuple(unstable)