import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;

public class WarehouseMovementTracker {

    public enum MovementType {
        INBOUND,
        OUTBOUND,
        TRANSFER
    }

    public static final class Movement {
        private final String productId;
        private final String productName;
        private final MovementType type;
        private final int quantity;
        private final LocalDate date;
        private final String location;

        public Movement(String productId,
                        String productName,
                        MovementType type,
                        int quantity,
                        LocalDate date,
                        String location) {
            this.productId = Objects.requireNonNull(productId);
            this.productName = Objects.requireNonNull(productName);
            this.type = Objects.requireNonNull(type);
            this.date = Objects.requireNonNull(date);
            this.location = Objects.requireNonNull(location);

            if (quantity <= 0) {
                throw new IllegalArgumentException("Quantity must be positive");
            }
            this.quantity = quantity;
        }

        public String getProductId() {
            return productId;
        }

        public String getProductName() {
            return productName;
        }

        public MovementType getType() {
            return type;
        }

        public int getQuantity() {
            return quantity;
        }

        public LocalDate getDate() {
            return date;
        }

        public String getLocation() {
            return location;
        }
    }

    public static final class StockSnapshot {
        private final String productId;
        private final String productName;
        private int balance;
        private LocalDate lastMovementDate;

        public StockSnapshot(String productId, String productName) {
            this.productId = productId;
            this.productName = productName;
            this.balance = 0;
        }

        public void apply(Movement movement) {
            switch (movement.getType()) {
                case INBOUND:
                    balance += movement.getQuantity();
                    break;
                case OUTBOUND:
                    balance -= movement.getQuantity();
                    break;
                case TRANSFER:
                    // transfers don't affect global balance in this simplified model
                    break;
            }
            lastMovementDate = movement.getDate();
        }

        public String format() {
            long idleDays = lastMovementDate == null
                    ? -1
                    : ChronoUnit.DAYS.between(lastMovementDate, LocalDate.now());

            return productId +
                    " | " + productName +
                    " | balance=" + balance +
                    " | lastMove=" + lastMovementDate +
                    " | idleDays=" + idleDays;
        }

        public int getBalance() {
            return balance;
        }
    }

    public static final class InventoryReport {
        private final List<StockSnapshot> snapshots;

        public InventoryReport(List<StockSnapshot> snapshots) {
            this.snapshots = new ArrayList<>(snapshots);
        }

        public String render() {
            StringBuilder sb = new StringBuilder();
            sb.append("Inventory Snapshot").append('\n');
            sb.append("------------------").append('\n');

            for (StockSnapshot s : snapshots) {
                sb.append(s.format()).append('\n');
            }

            return sb.toString();
        }
    }

    public InventoryReport buildSnapshot(List<Movement> movements) {
        List<StockSnapshot> snapshots = new ArrayList<>();

        for (Movement movement : movements) {
            StockSnapshot snapshot = findOrCreate(snapshots, movement);
            snapshot.apply(movement);
        }

        snapshots.sort(Comparator.comparingInt(StockSnapshot::getBalance).reversed());
        return new InventoryReport(snapshots);
    }

    private StockSnapshot findOrCreate(List<StockSnapshot> snapshots, Movement movement) {
        for (StockSnapshot s : snapshots) {
            if (s.productId.equals(movement.getProductId())) {
                return s;
            }
        }
        StockSnapshot created = new StockSnapshot(
                movement.getProductId(),
                movement.getProductName()
        );
        snapshots.add(created);
        return created;
    }

    public static void main(String[] args) {
        List<Movement> movements = List.of(
                new Movement("P-100", "Steel Bolts", MovementType.INBOUND, 500, LocalDate.of(2026, 3, 1), "WH-A"),
                new Movement("P-100", "Steel Bolts", MovementType.OUTBOUND, 120, LocalDate.of(2026, 3, 5), "WH-A"),
                new Movement("P-200", "Copper Wire", MovementType.INBOUND, 300, LocalDate.of(2026, 3, 2), "WH-B"),
                new Movement("P-200", "Copper Wire", MovementType.OUTBOUND, 50, LocalDate.of(2026, 3, 6), "WH-B"),
                new Movement("P-300", "Plastic Caps", MovementType.INBOUND, 800, LocalDate.of(2026, 3, 3), "WH-A"),
                new Movement("P-100", "Steel Bolts", MovementType.TRANSFER, 50, LocalDate.of(2026, 3, 7), "WH-C")
        );

        WarehouseMovementTracker tracker = new WarehouseMovementTracker();
        InventoryReport report = tracker.buildSnapshot(movements);

        System.out.println(report.render());
    }
}