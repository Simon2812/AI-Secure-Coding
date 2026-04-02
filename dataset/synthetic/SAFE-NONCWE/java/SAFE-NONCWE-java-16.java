import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;

public class JobDispatcher {

    public enum Priority {
        HIGH,
        MEDIUM,
        LOW
    }

    private static class Job {
        final String id;
        final Priority priority;
        final Instant readyAt;
        final int estimatedMillis;

        Job(String id, Priority priority, Instant readyAt, int estimatedMillis) {
            this.id = id;
            this.priority = priority;
            this.readyAt = readyAt;
            this.estimatedMillis = estimatedMillis;
        }
    }

    private static class RunningJob {
        final Job job;
        long remaining;

        RunningJob(Job job) {
            this.job = job;
            this.remaining = job.estimatedMillis;
        }
    }

    private final PriorityQueue<Job> queue = new PriorityQueue<>(
            (a, b) -> {
                int pr = a.priority.compareTo(b.priority);
                if (pr != 0) return pr;
                return a.readyAt.compareTo(b.readyAt);
            }
    );

    private final List<RunningJob> active = new ArrayList<>();
    private final List<String> completed = new ArrayList<>();

    private int maxParallel = 2;

    public void setMaxParallel(int maxParallel) {
        this.maxParallel = maxParallel;
    }

    public void submit(String id, Priority priority, Instant readyAt, int estimatedMillis) {
        queue.add(new Job(id, priority, readyAt, estimatedMillis));
    }

    public void tick(Instant now, int millisStep) {
        startEligible(now);
        advanceRunning(millisStep);
    }

    private void startEligible(Instant now) {
        while (active.size() < maxParallel && !queue.isEmpty()) {
            Job next = queue.peek();

            if (next.readyAt.isAfter(now)) {
                break;
            }

            queue.poll();
            active.add(new RunningJob(next));
        }
    }

    private void advanceRunning(int millisStep) {
        List<RunningJob> finished = new ArrayList<>();

        for (RunningJob r : active) {
            r.remaining -= millisStep;
            if (r.remaining <= 0) {
                finished.add(r);
            }
        }

        for (RunningJob r : finished) {
            active.remove(r);
            completed.add(r.job.id);
        }
    }

    public List<String> drainCompleted() {
        List<String> out = new ArrayList<>(completed);
        completed.clear();
        return out;
    }

    public int queuedCount() {
        return queue.size();
    }

    public int runningCount() {
        return active.size();
    }

    public boolean isIdle() {
        return queue.isEmpty() && active.isEmpty();
    }

    public static JobDispatcher demoSetup() {
        JobDispatcher dispatcher = new JobDispatcher();

        Instant base = Instant.now();

        dispatcher.submit("job-A", Priority.HIGH, base, 120);
        dispatcher.submit("job-B", Priority.MEDIUM, base.plusMillis(50), 200);
        dispatcher.submit("job-C", Priority.LOW, base, 300);
        dispatcher.submit("job-D", Priority.HIGH, base.plusMillis(20), 80);

        return dispatcher;
    }
}