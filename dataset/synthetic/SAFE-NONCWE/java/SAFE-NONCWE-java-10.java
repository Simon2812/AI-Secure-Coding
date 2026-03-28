import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;

public class EventStreamPipeline {

    interface Stage<I, O> {
        O process(I input);
    }

    static class MapStage<I, O> implements Stage<I, O> {
        private final Transformer<I, O> fn;

        public MapStage(Transformer<I, O> fn) {
            this.fn = fn;
        }

        @Override
        public O process(I input) {
            return fn.apply(input);
        }
    }

    static class FilterStage<T> implements Stage<T, T> {
        private final Predicate<T> predicate;

        public FilterStage(Predicate<T> predicate) {
            this.predicate = predicate;
        }

        @Override
        public T process(T input) {
            return predicate.test(input) ? input : null;
        }
    }

    interface Transformer<I, O> {
        O apply(I input);
    }

    interface Predicate<T> {
        boolean test(T value);
    }

    static class Pipeline<T> implements Iterable<T> {
        private final Iterable<T> source;
        private final List<Stage<?, ?>> stages;

        public Pipeline(Iterable<T> source) {
            this.source = source;
            this.stages = new ArrayList<>();
        }

        public <R> Pipeline<R> map(Transformer<T, R> fn) {
            Pipeline<R> next = new Pipeline<>(source);
            next.stages.addAll(this.stages);
            next.stages.add(new MapStage<>(fn));
            return next;
        }

        public Pipeline<T> filter(Predicate<T> predicate) {
            this.stages.add(new FilterStage<>(predicate));
            return this;
        }

        @Override
        public Iterator<T> iterator() {
            return new Iterator<>() {
                private final Iterator<T> it = source.iterator();
                private T nextItem;
                private boolean prepared = false;

                @Override
                public boolean hasNext() {
                    if (prepared) return nextItem != null;
                    nextItem = advance();
                    prepared = true;
                    return nextItem != null;
                }

                @Override
                public T next() {
                    if (!hasNext()) throw new NoSuchElementException();
                    prepared = false;
                    return nextItem;
                }

                @SuppressWarnings("unchecked")
                private T advance() {
                    while (it.hasNext()) {
                        Object current = it.next();

                        for (Stage<?, ?> stage : stages) {
                            current = ((Stage<Object, Object>) stage).process(current);
                            if (current == null) break;
                        }

                        if (current != null) {
                            return (T) current;
                        }
                    }
                    return null;
                }
            };
        }
    }

    public static void main(String[] args) {
        List<String> events = List.of(
                "login:user1",
                "click:home",
                "login:user2",
                "logout:user1",
                "click:profile",
                "login:user3"
        );

        Pipeline<String> pipeline = new Pipeline<>(events)
                .filter(e -> e.startsWith("login"))
                .map(e -> e.split(":")[1])
                .map(name -> name.toUpperCase());

        for (String user : pipeline) {
            System.out.println("LOGIN -> " + user);
        }
    }
}