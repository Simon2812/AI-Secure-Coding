import java.time.Instant;
import java.util.Objects;

public class TokenBucketLimiter {

    private final double capacity;
    private final double refillPerSecond;

    private double tokens;
    private Instant lastRefill;

    public TokenBucketLimiter(double capacity, double refillPerSecond) {
        if (capacity <= 0 || refillPerSecond <= 0) {
            throw new IllegalArgumentException("capacity and refill rate must be positive");
        }
        this.capacity = capacity;
        this.refillPerSecond = refillPerSecond;
        this.tokens = capacity;
        this.lastRefill = Instant.now();
    }

    public boolean tryConsume(double amount, Instant now) {
        Objects.requireNonNull(now);

        if (amount <= 0) {
            throw new IllegalArgumentException("amount must be positive");
        }

        refill(now);

        if (tokens >= amount) {
            tokens -= amount;
            return true;
        }

        return false;
    }

    public double estimateWaitSeconds(double amount, Instant now) {
        Objects.requireNonNull(now);

        if (amount <= 0) {
            return 0.0;
        }

        refill(now);

        if (tokens >= amount) {
            return 0.0;
        }

        double deficit = amount - tokens;
        return deficit / refillPerSecond;
    }

    public double available(Instant now) {
        refill(now);
        return tokens;
    }

    private void refill(Instant now) {
        long millis = now.toEpochMilli() - lastRefill.toEpochMilli();
        if (millis <= 0) {
            return;
        }

        double seconds = millis / 1000.0;
        double added = seconds * refillPerSecond;

        tokens = Math.min(capacity, tokens + added);
        lastRefill = now;
    }

    public void forceConsume(double amount) {
        tokens = Math.max(0, tokens - amount);
    }

    public void reset() {
        tokens = capacity;
        lastRefill = Instant.now();
    }

    public double capacity() {
        return capacity;
    }

    public double refillRate() {
        return refillPerSecond;
    }
}