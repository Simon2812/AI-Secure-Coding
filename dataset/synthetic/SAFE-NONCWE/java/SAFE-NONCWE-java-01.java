import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

public class InvoiceSummaryService {

    public static final class Invoice {
        private final String invoiceNumber;
        private final String customerName;
        private final LocalDate issuedOn;
        private final List<InvoiceLine> lines;

        public Invoice(String invoiceNumber, String customerName, LocalDate issuedOn, List<InvoiceLine> lines) {
            this.invoiceNumber = Objects.requireNonNull(invoiceNumber);
            this.customerName = Objects.requireNonNull(customerName);
            this.issuedOn = Objects.requireNonNull(issuedOn);
            this.lines = new ArrayList<>(Objects.requireNonNull(lines));
        }

        public String getInvoiceNumber() {
            return invoiceNumber;
        }

        public String getCustomerName() {
            return customerName;
        }

        public LocalDate getIssuedOn() {
            return issuedOn;
        }

        public List<InvoiceLine> getLines() {
            return Collections.unmodifiableList(lines);
        }
    }

    public static final class InvoiceLine {
        private final String sku;
        private final String description;
        private final Category category;
        private final int quantity;
        private final BigDecimal unitPrice;
        private final BigDecimal discountRate;

        public InvoiceLine(
                String sku,
                String description,
                Category category,
                int quantity,
                BigDecimal unitPrice,
                BigDecimal discountRate
        ) {
            this.sku = Objects.requireNonNull(sku);
            this.description = Objects.requireNonNull(description);
            this.category = Objects.requireNonNull(category);
            this.quantity = quantity;
            this.unitPrice = Objects.requireNonNull(unitPrice);
            this.discountRate = Objects.requireNonNull(discountRate);

            if (quantity <= 0) {
                throw new IllegalArgumentException("Quantity must be positive");
            }
            if (unitPrice.signum() < 0) {
                throw new IllegalArgumentException("Unit price must not be negative");
            }
            if (discountRate.signum() < 0 || discountRate.compareTo(BigDecimal.ONE) > 0) {
                throw new IllegalArgumentException("Discount rate must be between 0 and 1");
            }
        }

        public String getSku() {
            return sku;
        }

        public String getDescription() {
            return description;
        }

        public Category getCategory() {
            return category;
        }

        public int getQuantity() {
            return quantity;
        }

        public BigDecimal getUnitPrice() {
            return unitPrice;
        }

        public BigDecimal getDiscountRate() {
            return discountRate;
        }

        public BigDecimal getGrossAmount() {
            return unitPrice.multiply(BigDecimal.valueOf(quantity));
        }

        public BigDecimal getDiscountAmount() {
            return getGrossAmount().multiply(discountRate).setScale(2, RoundingMode.HALF_UP);
        }

        public BigDecimal getNetAmount() {
            return getGrossAmount().subtract(getDiscountAmount()).setScale(2, RoundingMode.HALF_UP);
        }
    }

    public enum Category {
        HARDWARE,
        SOFTWARE,
        SERVICE,
        TRAINING,
        SHIPPING
    }

    public static final class InvoiceSummary {
        private final String invoiceNumber;
        private final String customerName;
        private final LocalDate issuedOn;
        private final int totalUnits;
        private final BigDecimal grossTotal;
        private final BigDecimal discountTotal;
        private final BigDecimal netTotal;
        private final Map<Category, BigDecimal> categoryTotals;
        private final List<LineBreakdown> topLines;

        public InvoiceSummary(
                String invoiceNumber,
                String customerName,
                LocalDate issuedOn,
                int totalUnits,
                BigDecimal grossTotal,
                BigDecimal discountTotal,
                BigDecimal netTotal,
                Map<Category, BigDecimal> categoryTotals,
                List<LineBreakdown> topLines
        ) {
            this.invoiceNumber = invoiceNumber;
            this.customerName = customerName;
            this.issuedOn = issuedOn;
            this.totalUnits = totalUnits;
            this.grossTotal = grossTotal;
            this.discountTotal = discountTotal;
            this.netTotal = netTotal;
            this.categoryTotals = new EnumMap<>(categoryTotals);
            this.topLines = new ArrayList<>(topLines);
        }

        public String formatAsReport() {
            StringBuilder sb = new StringBuilder();
            sb.append("Invoice Summary").append('\n');
            sb.append("---------------").append('\n');
            sb.append("Invoice Number : ").append(invoiceNumber).append('\n');
            sb.append("Customer       : ").append(customerName).append('\n');
            sb.append("Issued On      : ").append(issuedOn).append('\n');
            sb.append("Total Units    : ").append(totalUnits).append('\n');
            sb.append("Gross Total    : ").append(grossTotal).append('\n');
            sb.append("Discount Total : ").append(discountTotal).append('\n');
            sb.append("Net Total      : ").append(netTotal).append('\n');
            sb.append('\n');

            sb.append("Category Totals").append('\n');
            sb.append("---------------").append('\n');
            for (Map.Entry<Category, BigDecimal> entry : categoryTotals.entrySet()) {
                sb.append(padRight(entry.getKey().name(), 12))
                  .append(" : ")
                  .append(entry.getValue())
                  .append('\n');
            }

            sb.append('\n');
            sb.append("Top Lines by Net Amount").append('\n');
            sb.append("-----------------------").append('\n');
            for (LineBreakdown line : topLines) {
                sb.append(line.format()).append('\n');
            }

            return sb.toString();
        }

        private static String padRight(String value, int width) {
            StringBuilder sb = new StringBuilder(value);
            while (sb.length() < width) {
                sb.append(' ');
            }
            return sb.toString();
        }
    }

    public static final class LineBreakdown {
        private final String sku;
        private final String description;
        private final int quantity;
        private final BigDecimal netAmount;

        public LineBreakdown(String sku, String description, int quantity, BigDecimal netAmount) {
            this.sku = sku;
            this.description = description;
            this.quantity = quantity;
            this.netAmount = netAmount;
        }

        public BigDecimal getNetAmount() {
            return netAmount;
        }

        public String format() {
            return sku + " | " + description + " | qty=" + quantity + " | net=" + netAmount;
        }
    }

    public InvoiceSummary summarize(Invoice invoice) {
        int totalUnits = 0;
        BigDecimal grossTotal = BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP);
        BigDecimal discountTotal = BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP);
        BigDecimal netTotal = BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP);
        Map<Category, BigDecimal> categoryTotals = initializeCategoryTotals();
        List<LineBreakdown> lineBreakdowns = new ArrayList<>();

        for (InvoiceLine line : invoice.getLines()) {
            totalUnits += line.getQuantity();
            grossTotal = grossTotal.add(line.getGrossAmount()).setScale(2, RoundingMode.HALF_UP);
            discountTotal = discountTotal.add(line.getDiscountAmount()).setScale(2, RoundingMode.HALF_UP);
            netTotal = netTotal.add(line.getNetAmount()).setScale(2, RoundingMode.HALF_UP);

            BigDecimal currentCategoryTotal = categoryTotals.get(line.getCategory());
            categoryTotals.put(
                    line.getCategory(),
                    currentCategoryTotal.add(line.getNetAmount()).setScale(2, RoundingMode.HALF_UP)
            );

            lineBreakdowns.add(new LineBreakdown(
                    line.getSku(),
                    line.getDescription(),
                    line.getQuantity(),
                    line.getNetAmount()
            ));
        }

        lineBreakdowns.sort(Comparator.comparing(LineBreakdown::getNetAmount).reversed());

        List<LineBreakdown> topLines = new ArrayList<>();
        for (int i = 0; i < lineBreakdowns.size() && i < 5; i++) {
            topLines.add(lineBreakdowns.get(i));
        }

        return new InvoiceSummary(
                invoice.getInvoiceNumber(),
                invoice.getCustomerName(),
                invoice.getIssuedOn(),
                totalUnits,
                grossTotal,
                discountTotal,
                netTotal,
                categoryTotals,
                topLines
        );
    }

    private Map<Category, BigDecimal> initializeCategoryTotals() {
        Map<Category, BigDecimal> totals = new EnumMap<>(Category.class);
        for (Category category : Category.values()) {
            totals.put(category, BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP));
        }
        return totals;
    }

    public static void main(String[] args) {
        List<InvoiceLine> lines = List.of(
                new InvoiceLine(
                        "HW-1042",
                        "27-inch office monitor",
                        Category.HARDWARE,
                        3,
                        new BigDecimal("189.90"),
                        new BigDecimal("0.05")
                ),
                new InvoiceLine(
                        "SV-2300",
                        "Quarterly onboarding workshop",
                        Category.TRAINING,
                        2,
                        new BigDecimal("420.00"),
                        new BigDecimal("0.10")
                ),
                new InvoiceLine(
                        "SS-9910",
                        "Deployment assistance",
                        Category.SERVICE,
                        5,
                        new BigDecimal("115.00"),
                        new BigDecimal("0.00")
                ),
                new InvoiceLine(
                        "LG-1001",
                        "Regional shipping batch",
                        Category.SHIPPING,
                        1,
                        new BigDecimal("49.99"),
                        new BigDecimal("0.00")
                ),
                new InvoiceLine(
                        "SW-3105",
                        "Team collaboration seats",
                        Category.SOFTWARE,
                        12,
                        new BigDecimal("24.50"),
                        new BigDecimal("0.15")
                )
        );

        Invoice invoice = new Invoice(
                "INV-2026-031",
                "Northwind Design Studio",
                LocalDate.of(2026, 3, 24),
                lines
        );

        InvoiceSummaryService service = new InvoiceSummaryService();
        InvoiceSummary summary = service.summarize(invoice);

        System.out.println(summary.formatAsReport());
    }
}