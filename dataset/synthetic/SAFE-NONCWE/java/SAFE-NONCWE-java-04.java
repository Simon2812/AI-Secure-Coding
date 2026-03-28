import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;

public class SubscriptionRenewalManager {

    public enum PlanType {
        BASIC,
        STANDARD,
        PREMIUM
    }

    public static final class Subscription {
        private final String id;
        private final String customer;
        private final PlanType planType;
        private final LocalDate startDate;
        private final int billingCycleDays;
        private boolean active;

        public Subscription(
                String id,
                String customer,
                PlanType planType,
                LocalDate startDate,
                int billingCycleDays,
                boolean active
        ) {
            this.id = Objects.requireNonNull(id);
            this.customer = Objects.requireNonNull(customer);
            this.planType = Objects.requireNonNull(planType);
            this.startDate = Objects.requireNonNull(startDate);
            this.billingCycleDays = billingCycleDays;
            this.active = active;

            if (billingCycleDays <= 0) {
                throw new IllegalArgumentException("Billing cycle must be positive");
            }
        }

        public String getId() {
            return id;
        }

        public String getCustomer() {
            return customer;
        }

        public PlanType getPlanType() {
            return planType;
        }

        public LocalDate getStartDate() {
            return startDate;
        }

        public int getBillingCycleDays() {
            return billingCycleDays;
        }

        public boolean isActive() {
            return active;
        }

        public void deactivate() {
            this.active = false;
        }
    }

    public static final class RenewalInfo {
        private final Subscription subscription;
        private final LocalDate nextRenewal;
        private final long daysRemaining;
        private final String urgency;

        public RenewalInfo(Subscription subscription, LocalDate nextRenewal, long daysRemaining, String urgency) {
            this.subscription = subscription;
            this.nextRenewal = nextRenewal;
            this.daysRemaining = daysRemaining;
            this.urgency = urgency;
        }

        public String format() {
            return subscription.getId() +
                    " | " + subscription.getCustomer() +
                    " | " + subscription.getPlanType() +
                    " | renew=" + nextRenewal +
                    " | daysLeft=" + daysRemaining +
                    " | " + urgency;
        }

        public long getDaysRemaining() {
            return daysRemaining;
        }
    }

    public static final class RenewalReport {
        private final List<RenewalInfo> entries;

        public RenewalReport(List<RenewalInfo> entries) {
            this.entries = new ArrayList<>(entries);
        }

        public String render() {
            StringBuilder sb = new StringBuilder();
            sb.append("Renewal Schedule").append('\n');
            sb.append("----------------").append('\n');

            for (RenewalInfo info : entries) {
                sb.append(info.format()).append('\n');
            }

            return sb.toString();
        }
    }

    public RenewalReport buildReport(List<Subscription> subscriptions, LocalDate today) {
        List<RenewalInfo> result = new ArrayList<>();

        for (Subscription sub : subscriptions) {
            if (!sub.isActive()) {
                continue;
            }

            LocalDate nextRenewal = calculateNextRenewal(sub, today);
            long daysLeft = ChronoUnit.DAYS.between(today, nextRenewal);

            result.add(new RenewalInfo(
                    sub,
                    nextRenewal,
                    daysLeft,
                    classify(daysLeft)
            ));
        }

        result.sort(Comparator.comparingLong(RenewalInfo::getDaysRemaining));

        return new RenewalReport(result);
    }

    private LocalDate calculateNextRenewal(Subscription sub, LocalDate today) {
        LocalDate cyclePoint = sub.getStartDate();

        while (!cyclePoint.isAfter(today)) {
            cyclePoint = cyclePoint.plusDays(sub.getBillingCycleDays());
        }

        return cyclePoint;
    }

    private String classify(long daysLeft) {
        if (daysLeft <= 3) return "CRITICAL";
        if (daysLeft <= 7) return "HIGH";
        if (daysLeft <= 14) return "MEDIUM";
        return "LOW";
    }

    public static void main(String[] args) {
        List<Subscription> subs = List.of(
                new Subscription(
                        "SUB-001",
                        "Green Market Ltd",
                        PlanType.STANDARD,
                        LocalDate.of(2026, 1, 10),
                        30,
                        true
                ),
                new Subscription(
                        "SUB-002",
                        "Urban Fitness",
                        PlanType.PREMIUM,
                        LocalDate.of(2026, 2, 5),
                        30,
                        true
                ),
                new Subscription(
                        "SUB-003",
                        "Local Bakery",
                        PlanType.BASIC,
                        LocalDate.of(2025, 12, 20),
                        15,
                        true
                ),
                new Subscription(
                        "SUB-004",
                        "Studio North",
                        PlanType.PREMIUM,
                        LocalDate.of(2026, 1, 1),
                        30,
                        false
                )
        );

        SubscriptionRenewalManager manager = new SubscriptionRenewalManager();
        RenewalReport report = manager.buildReport(subs, LocalDate.of(2026, 3, 28));

        System.out.println(report.render());
    }
}