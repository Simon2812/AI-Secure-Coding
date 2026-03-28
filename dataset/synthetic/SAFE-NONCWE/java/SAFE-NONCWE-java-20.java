import java.time.Duration;
import java.time.Instant;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.LinkedHashMap;
import java.util.Map;

public class RollingEventMetrics {

    public enum Severity {
        INFO,
        WARN,
        ERROR
    }

    public static final class MetricSnapshot {
        private final int totalEvents;
        private final int infoCount;
        private final int warnCount;
        private final int errorCount;
        private final double averageLatencyMs;
        private final long maxLatencyMs;
        private final Map<String, Integer> countsByCategory;

        MetricSnapshot(
                int totalEvents,
                int infoCount,
                int warnCount,
                int errorCount,
                double averageLatencyMs,
                long maxLatencyMs,
                Map<String, Integer> countsByCategory
        ) {
            this.totalEvents = totalEvents;
            this.infoCount = infoCount;
            this.warnCount = warnCount;
            this.errorCount = errorCount;
            this.averageLatencyMs = averageLatencyMs;
            this.maxLatencyMs = maxLatencyMs;
            this.countsByCategory = countsByCategory;
        }

        public int getTotalEvents() {
            return totalEvents;
        }

        public int getInfoCount() {
            return infoCount;
        }

        public int getWarnCount() {
            return warnCount;
        }

        public int getErrorCount() {
            return errorCount;
        }

        public double getAverageLatencyMs() {
            return averageLatencyMs;
        }

        public long getMaxLatencyMs() {
            return maxLatencyMs;
        }

        public Map<String, Integer> getCountsByCategory() {
            return new LinkedHashMap<>(countsByCategory);
        }
    }

    private static final class EventRecord {
        final Instant timestamp;
        final String category;
        final Severity severity;
        final long latencyMs;

        EventRecord(Instant timestamp, String category, Severity severity, long latencyMs) {
            this.timestamp = timestamp;
            this.category = category;
            this.severity = severity;
            this.latencyMs = latencyMs;
        }
    }

    private final Duration window;
    private final Deque<EventRecord> events = new ArrayDeque<>();
    private final Map<String, Integer> categoryCounters = new LinkedHashMap<>();

    private int infoCount;
    private int warnCount;
    private int errorCount;
    private long totalLatency;
    private long maxLatency;

    public RollingEventMetrics(Duration window) {
        if (window == null || window.isNegative() || window.isZero()) {
            throw new IllegalArgumentException("window must be positive");
        }
        this.window = window;
    }

    public void add(Instant timestamp, String category, Severity severity, long latencyMs) {
        if (timestamp == null) {
            throw new IllegalArgumentException("timestamp must not be null");
        }
        if (category == null || category.isBlank()) {
            throw new IllegalArgumentException("category must not be blank");
        }
        if (severity == null) {
            throw new IllegalArgumentException("severity must not be null");
        }
        if (latencyMs < 0) {
            throw new IllegalArgumentException("latency must not be negative");
        }

        EventRecord record = new EventRecord(timestamp, category, severity, latencyMs);
        events.addLast(record);

        switch (severity) {
            case INFO -> infoCount++;
            case WARN -> warnCount++;
            case ERROR -> errorCount++;
        }

        categoryCounters.merge(category, 1, Integer::sum);
        totalLatency += latencyMs;
        if (latencyMs > maxLatency) {
            maxLatency = latencyMs;
        }
    }

    public void evictExpired(Instant now) {
        if (now == null) {
            throw new IllegalArgumentException("now must not be null");
        }

        Instant threshold = now.minus(window);

        while (!events.isEmpty()) {
            EventRecord oldest = events.peekFirst();
            if (!oldest.timestamp.isBefore(threshold)) {
                break;
            }

            events.removeFirst();

            switch (oldest.severity) {
                case INFO -> infoCount--;
                case WARN -> warnCount--;
                case ERROR -> errorCount--;
            }

            decrementCategory(oldest.category);
            totalLatency -= oldest.latencyMs;
        }

        recomputeMaxLatencyIfNeeded();
    }

    public MetricSnapshot snapshot() {
        int total = events.size();
        double avg = total == 0 ? 0.0 : (double) totalLatency / total;

        return new MetricSnapshot(
                total,
                infoCount,
                warnCount,
                errorCount,
                avg,
                maxLatency,
                new LinkedHashMap<>(categoryCounters)
        );
    }

    public int size() {
        return events.size();
    }

    public boolean isEmpty() {
        return events.isEmpty();
    }

    private void decrementCategory(String category) {
        Integer count = categoryCounters.get(category);
        if (count == null) {
            return;
        }

        if (count == 1) {
            categoryCounters.remove(category);
        } else {
            categoryCounters.put(category, count - 1);
        }
    }

    private void recomputeMaxLatencyIfNeeded() {
        long currentMax = 0;
        for (EventRecord record : events) {
            if (record.latencyMs > currentMax) {
                currentMax = record.latencyMs;
            }
        }
        maxLatency = currentMax;
    }

    public static RollingEventMetrics createForLastFiveMinutes() {
        return new RollingEventMetrics(Duration.ofMinutes(5));
    }
}