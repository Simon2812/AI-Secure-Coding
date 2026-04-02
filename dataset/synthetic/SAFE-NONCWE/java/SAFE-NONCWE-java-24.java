import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

public class ConfigDiffTracker {

    public static final class ChangeSet {
        private final Map<String, String> added = new HashMap<>();
        private final Map<String, String> removed = new HashMap<>();
        private final Map<String, ValueChange> modified = new HashMap<>();

        public Map<String, String> added() {
            return new HashMap<>(added);
        }

        public Map<String, String> removed() {
            return new HashMap<>(removed);
        }

        public Map<String, ValueChange> modified() {
            return new HashMap<>(modified);
        }

        public boolean isEmpty() {
            return added.isEmpty() && removed.isEmpty() && modified.isEmpty();
        }
    }

    public static final class ValueChange {
        private final String oldValue;
        private final String newValue;

        ValueChange(String oldValue, String newValue) {
            this.oldValue = oldValue;
            this.newValue = newValue;
        }

        public String oldValue() {
            return oldValue;
        }

        public String newValue() {
            return newValue;
        }
    }

    public ChangeSet compare(
            Map<String, String> previous,
            Map<String, String> current
    ) {
        Objects.requireNonNull(previous);
        Objects.requireNonNull(current);

        ChangeSet changes = new ChangeSet();

        // Detect removed and modified
        for (Map.Entry<String, String> entry : previous.entrySet()) {
            String key = entry.getKey();
            String oldValue = entry.getValue();

            if (!current.containsKey(key)) {
                changes.removed.put(key, oldValue);
                continue;
            }

            String newValue = current.get(key);
            if (!equals(oldValue, newValue)) {
                changes.modified.put(key, new ValueChange(oldValue, newValue));
            }
        }

        // Detect added
        for (Map.Entry<String, String> entry : current.entrySet()) {
            String key = entry.getKey();

            if (!previous.containsKey(key)) {
                changes.added.put(key, entry.getValue());
            }
        }

        return changes;
    }

    public Map<String, String> applyPatch(
            Map<String, String> base,
            ChangeSet changes
    ) {
        Map<String, String> result = new HashMap<>(base);

        for (Map.Entry<String, String> entry : changes.removed.entrySet()) {
            result.remove(entry.getKey());
        }

        for (Map.Entry<String, String> entry : changes.added.entrySet()) {
            result.put(entry.getKey(), entry.getValue());
        }

        for (Map.Entry<String, ValueChange> entry : changes.modified.entrySet()) {
            result.put(entry.getKey(), entry.getValue().newValue());
        }

        return result;
    }

    public boolean hasBreakingChanges(ChangeSet changes) {
        for (String key : changes.removed.keySet()) {
            if (isCriticalKey(key)) {
                return true;
            }
        }

        for (Map.Entry<String, ValueChange> entry : changes.modified.entrySet()) {
            if (isCriticalKey(entry.getKey())) {
                return true;
            }
        }

        return false;
    }

    private boolean isCriticalKey(String key) {
        // simple heuristic: keys containing "timeout" or "endpoint" are critical
        return key.contains("timeout") || key.contains("endpoint");
    }

    private boolean equals(String a, String b) {
        if (a == null) return b == null;
        return a.equals(b);
    }
}