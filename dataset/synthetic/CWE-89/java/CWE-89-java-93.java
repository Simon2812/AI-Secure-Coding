public class InvoiceSortQuery {

    private final java.sql.DataSource ds;

    public InvoiceSortQuery(java.sql.DataSource ds) {
        this.ds = ds;
    }

    private String safeOrderBy(String sortKey) {
        if (sortKey == null) return "invoice_id";
        return switch (sortKey) {
            case "date" -> "bill_month";
            case "total" -> "total";
            case "id" -> "invoice_id";
            default -> "invoice_id";
        };
    }

    public java.util.List<String> list(String accountId, String sortKey) throws Exception {
        String order = safeOrderBy(sortKey);
        String sql = "SELECT invoice_id, bill_month, total FROM invoices WHERE account_id=? ORDER BY " + order;

        java.util.ArrayList<String> out = new java.util.ArrayList<>();

        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {

            ps.setString(1, accountId);
            try (java.sql.ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    out.add(rs.getString(1) + "," + rs.getString(2) + "," + rs.getBigDecimal(3));
                }
            }
        }

        return out;
    }
}