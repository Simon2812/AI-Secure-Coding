from collections import defaultdict


class StateMachine:
    def __init__(self):
        self._transitions = defaultdict(list)
        self._initial = None
        self._terminal = set()

    def set_initial(self, state):
        self._initial = state

    def add_terminal(self, state):
        self._terminal.add(state)

    def add_transition(self, source, target, condition, label):
        self._transitions[source].append((target, condition, label))

    def next_state(self, current, context):
        for target, condition, label in self._transitions.get(current, []):
            if condition(context):
                return target, label
        return current, None

    def is_terminal(self, state):
        return state in self._terminal


class Context:
    def __init__(self, user_id):
        self.user_id = user_id
        self.data = {}
        self.history = []
        self.flags = set()

    def update(self, key, value):
        self.data[key] = value

    def mark(self, flag):
        self.flags.add(flag)

    def record(self, state, action):
        self.history.append((state, action))


class WorkflowEngine:
    def __init__(self, machine):
        self._machine = machine

    def run(self, context, max_steps=50):
        state = self._machine._initial

        for _ in range(max_steps):
            if self._machine.is_terminal(state):
                context.record(state, "terminal")
                break

            next_state, action = self._machine.next_state(state, context)

            if action:
                context.record(state, action)

            if next_state == state:
                context.record(state, "stalled")
                break

            state = next_state

        return state


def has_profile(context):
    return bool(context.data.get("profile_complete"))


def has_verified_email(context):
    return bool(context.data.get("email_verified"))


def has_uploaded_docs(context):
    return bool(context.data.get("documents_uploaded"))


def risk_detected(context):
    return context.data.get("risk_score", 0) > 7


def low_activity(context):
    return context.data.get("activity_events", 0) < 2


def build_onboarding_machine():
    sm = StateMachine()

    sm.set_initial("start")

    sm.add_terminal("approved")
    sm.add_terminal("rejected")
    sm.add_terminal("abandoned")

    sm.add_transition("start", "profile", lambda c: True, "begin")

    sm.add_transition("profile", "verification", has_profile, "profile_complete")
    sm.add_transition("profile", "abandoned", low_activity, "inactive")

    sm.add_transition("verification", "documents", has_verified_email, "email_ok")
    sm.add_transition("verification", "rejected", risk_detected, "risk_fail")

    sm.add_transition("documents", "review", has_uploaded_docs, "docs_ok")
    sm.add_transition("documents", "abandoned", low_activity, "no_docs")

    sm.add_transition("review", "approved", lambda c: not risk_detected(c), "clear")
    sm.add_transition("review", "rejected", risk_detected, "risk_flag")

    return sm


class AuditTrail:
    def __init__(self, context):
        self._context = context

    def actions_by_state(self):
        grouped = defaultdict(list)

        for state, action in self._context.history:
            grouped[state].append(action)

        return dict(grouped)

    def transitions(self):
        seq = self._context.history
        result = []

        for i in range(len(seq) - 1):
            result.append((seq[i][0], seq[i + 1][0]))

        return tuple(result)

    def anomalies(self):
        issues = []

        seen = set()

        for state, action in self._context.history:
            if (state, action) in seen:
                issues.append((state, action, "repeated"))
            seen.add((state, action))

        return tuple(issues)


def summarize_context(context):
    return {
        "user": context.user_id,
        "flags": tuple(sorted(context.flags)),
        "steps": len(context.history),
        "final_state": context.history[-1][0] if context.history else None,
    }


def main():
    machine = build_onboarding_machine()
    engine = WorkflowEngine(machine)

    ctx = Context("user-42")

    ctx.update("profile_complete", True)
    ctx.update("email_verified", True)
    ctx.update("documents_uploaded", True)
    ctx.update("risk_score", 3)
    ctx.update("activity_events", 5)

    final_state = engine.run(ctx)

    audit = AuditTrail(ctx)

    print("Final state:", final_state)
    print("Summary:", summarize_context(ctx))
    print("Transitions:", audit.transitions())
    print("Anomalies:", audit.anomalies())


if __name__ == "__main__":
    main()