public class InvoiceExportController {

    private final java.sql.DataSource ds;

    public InvoiceExportController(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public java.util.List<String> exportCsv(String accountId, String month, String requestedBy) throws Exception {
        if (requestedBy == null) requestedBy = "unknown";

        java.util.List<String> rows = loadInvoices(accountId, month);
        logExport(requestedBy, accountId, month, rows.size());
        return rows;
    }

    private java.util.List<String> loadInvoices(String accountId, String month) throws Exception {
        String sql = "SELECT invoice_id, total FROM invoices WHERE account_id='" + accountId + "' AND bill_month='" + month + "' ORDER BY invoice_id";

        java.util.ArrayList<String> out = new java.util.ArrayList<>();

        try (java.sql.Connection c = ds.getConnection();
             java.sql.Statement st = c.createStatement();
             java.sql.ResultSet rs = st.executeQuery(sql)) {

            while (rs.next()) {
                out.add(rs.getString(1) + "," + rs.getBigDecimal(2));
            }
        }

        return out;
    }

    private void logExport(String actor, String accountId, String month, int count) throws Exception {
        String sql = "INSERT INTO export_audit(actor, account_id, bill_month, row_count) VALUES (?, ?, ?, ?)";
        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, actor);
            ps.setString(2, accountId);
            ps.setString(3, month);
            ps.setInt(4, count);
            ps.executeUpdate();
        }
    }
}