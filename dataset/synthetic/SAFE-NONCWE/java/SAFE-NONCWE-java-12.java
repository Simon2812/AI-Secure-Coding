import java.util.HashMap;
import java.util.Map;

public class TurnstileStateMachine {

    enum State {
        LOCKED,
        UNLOCKED,
        ALARM
    }

    enum Event {
        COIN,
        PUSH,
        FORCE,
        RESET
    }

    static class TransitionKey {
        final State state;
        final Event event;

        TransitionKey(State state, Event event) {
            this.state = state;
            this.event = event;
        }

        @Override
        public boolean equals(Object o) {
            if (!(o instanceof TransitionKey k)) return false;
            return k.state == state && k.event == event;
        }

        @Override
        public int hashCode() {
            return state.hashCode() * 31 + event.hashCode();
        }
    }

    static class Transition {
        final State nextState;
        final String action;

        Transition(State nextState, String action) {
            this.nextState = nextState;
            this.action = action;
        }
    }

    private final Map<TransitionKey, Transition> table = new HashMap<>();
    private State current = State.LOCKED;

    public TurnstileStateMachine() {
        register(State.LOCKED, Event.COIN, State.UNLOCKED, "unlock");
        register(State.LOCKED, Event.PUSH, State.LOCKED, "blocked");
        register(State.LOCKED, Event.FORCE, State.ALARM, "alarm");

        register(State.UNLOCKED, Event.PUSH, State.LOCKED, "lock");
        register(State.UNLOCKED, Event.COIN, State.UNLOCKED, "return_coin");
        register(State.UNLOCKED, Event.FORCE, State.ALARM, "alarm");

        register(State.ALARM, Event.RESET, State.LOCKED, "reset_alarm");
        register(State.ALARM, Event.COIN, State.ALARM, "ignore");
        register(State.ALARM, Event.PUSH, State.ALARM, "ignore");
    }

    private void register(State from, Event event, State to, String action) {
        table.put(new TransitionKey(from, event), new Transition(to, action));
    }

    public String handle(Event event) {
        Transition t = table.get(new TransitionKey(current, event));

        if (t == null) {
            return "no_transition (" + current + " + " + event + ")";
        }

        State previous = current;
        current = t.nextState;

        return previous + " --" + event + "/" + t.action + "--> " + current;
    }

    public State getState() {
        return current;
    }

    public static void main(String[] args) {
        TurnstileStateMachine machine = new TurnstileStateMachine();

        Event[] sequence = {
                Event.PUSH,
                Event.COIN,
                Event.PUSH,
                Event.FORCE,
                Event.COIN,
                Event.RESET,
                Event.COIN,
                Event.PUSH
        };

        for (Event e : sequence) {
            String result = machine.handle(e);
            System.out.println(result);
        }

        System.out.println("Final state: " + machine.getState());
    }
}