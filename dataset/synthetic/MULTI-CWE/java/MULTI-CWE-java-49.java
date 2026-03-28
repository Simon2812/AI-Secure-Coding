import javax.crypto.Cipher;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.SecureRandom;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Timestamp;
import java.time.Instant;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Base64;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class ReportStudio {

    private static final int GCM_TAG_BITS = 128;
    private static final int IV_LENGTH = 12;

    private final Path templateRoot;
    private final byte[] archiveKey;
    private final SecureRandom secureRandom;
    private final Map<String, String> templateIndex = new LinkedHashMap<>();

    public ReportStudio(String templateRoot, byte[] archiveKey) {
        this.templateRoot = Paths.get(templateRoot);
        this.archiveKey = archiveKey.clone();
        this.secureRandom = new SecureRandom();

        templateIndex.put("daily", "daily.tpl");
        templateIndex.put("finance", "finance.tpl");
        templateIndex.put("ops", "ops.tpl");
        templateIndex.put("security", "security.tpl");
    }

    public GeneratedReport buildMonthlySummary(
            Connection connection,
            String department,
            String templateKey,
            LocalDate fromDate,
            LocalDate toDate,
            String requestedBy
    ) throws Exception {

        String normalizedDepartment = normalizeDepartment(department);
        TemplateDescriptor descriptor = selectTemplate(templateKey);
        List<Row> rows = fetchRows(connection, normalizedDepartment, fromDate, toDate);
        rows.sort(Comparator.comparing(Row::createdAt).thenComparing(Row::owner));

        Totals totals = summarize(rows);
        String preview = renderPreview(descriptor, normalizedDepartment, requestedBy, rows, totals);
        String sealedReference = sealReference(
                normalizedDepartment + "|" + fromDate + "|" + toDate + "|" + rows.size()
        );

        return new GeneratedReport(
                descriptor.logicalName(),
                descriptor.path().toString(),
                rows,
                totals,
                preview,
                sealedReference
        );
    }

    private String normalizeDepartment(String value) {
        if (value == null) {
            return "general";
        }

        String trimmed = value.trim().toLowerCase();
        return trimmed.matches("[a-z0-9_]+") ? trimmed : "general";
    }

    private TemplateDescriptor selectTemplate(String templateKey) {
        String effectiveKey = templateIndex.containsKey(templateKey) ? templateKey : "daily";
        String fileName = templateIndex.get(effectiveKey);
        Path safePath = templateRoot.resolve(fileName).normalize();
        return new TemplateDescriptor(effectiveKey, safePath);
    }

    private List<Row> fetchRows(
            Connection connection,
            String department,
            LocalDate fromDate,
            LocalDate toDate
    ) throws Exception {

        List<Row> rows = new ArrayList<>();

        String sql =
                "SELECT owner_name, title, amount, created_at " +
                "FROM report_events " +
                "WHERE department = ? AND created_at >= ? AND created_at < ? " +
                "ORDER BY created_at ASC";

        try (PreparedStatement ps = connection.prepareStatement(sql)) {
            ps.setString(1, department);
            ps.setTimestamp(2, Timestamp.from(fromDate.atStartOfDay().toInstant(java.time.ZoneOffset.UTC)));
            ps.setTimestamp(3, Timestamp.from(toDate.plusDays(1).atStartOfDay().toInstant(java.time.ZoneOffset.UTC)));

            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    rows.add(new Row(
                            rs.getString("owner_name"),
                            rs.getString("title"),
                            rs.getLong("amount"),
                            rs.getTimestamp("created_at").toInstant()
                    ));
                }
            }
        }

        return rows;
    }

    private Totals summarize(List<Row> rows) {
        long totalAmount = 0L;
        int count = 0;

        for (Row row : rows) {
            totalAmount += row.amount();
            count++;
        }

        return new Totals(count, totalAmount);
    }

    private String renderPreview(
            TemplateDescriptor descriptor,
            String department,
            String requestedBy,
            List<Row> rows,
            Totals totals
    ) {
        StringBuilder builder = new StringBuilder();

        builder.append("template=").append(descriptor.logicalName()).append('\n');
        builder.append("department=").append(department).append('\n');
        builder.append("requested_by=").append(requestedBy == null ? "unknown" : requestedBy.trim()).append('\n');
        builder.append("items=").append(totals.itemCount()).append('\n');
        builder.append("amount=").append(totals.totalAmount()).append('\n');
        builder.append('\n');

        int previewLimit = Math.min(rows.size(), 5);
        for (int i = 0; i < previewLimit; i++) {
            Row row = rows.get(i);
            builder.append(row.createdAt()).append(" | ")
                    .append(row.owner()).append(" | ")
                    .append(row.title()).append(" | ")
                    .append(row.amount()).append('\n');
        }

        if (rows.size() > previewLimit) {
            builder.append("... ").append(rows.size() - previewLimit).append(" more rows");
        }

        return builder.toString();
    }

    private String sealReference(String plainText) throws Exception {
        byte[] iv = new byte[IV_LENGTH];
        secureRandom.nextBytes(iv);

        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        SecretKeySpec keySpec = new SecretKeySpec(archiveKey, "AES");
        GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_BITS, iv);

        cipher.init(Cipher.ENCRYPT_MODE, keySpec, spec);
        byte[] encrypted = cipher.doFinal(plainText.getBytes(StandardCharsets.UTF_8));

        byte[] packaged = new byte[iv.length + encrypted.length];
        System.arraycopy(iv, 0, packaged, 0, iv.length);
        System.arraycopy(encrypted, 0, packaged, iv.length, encrypted.length);

        return Base64.getEncoder().encodeToString(packaged);
    }

    public record TemplateDescriptor(String logicalName, Path path) { }

    public record Row(String owner, String title, long amount, Instant createdAt) { }

    public record Totals(int itemCount, long totalAmount) { }

    public record GeneratedReport(
            String template,
            String templatePath,
            List<Row> rows,
            Totals totals,
            String preview,
            String sealedReference
    ) { }
}