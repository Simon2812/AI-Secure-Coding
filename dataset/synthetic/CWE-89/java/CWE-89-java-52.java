public class InvoiceExportJob {

    private final java.sql.DataSource ds;

    public InvoiceExportJob(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public java.util.List<String> load(String customerId, String status) throws Exception {
        String sql = "SELECT id, amount FROM invoices WHERE customer_id='" + customerId + "'";
        if (status != null && !status.isBlank()) {
            sql += " AND status='" + status + "'";
        }

        java.util.ArrayList<String> out = new java.util.ArrayList<>();
        try (java.sql.Connection c = ds.getConnection();
             java.sql.Statement st = c.createStatement();
             java.sql.ResultSet rs = st.executeQuery(sql)) {

            while (rs.next()) {
                out.add(rs.getLong(1) + " " + rs.getBigDecimal(2));
            }
        }
        return out;
    }
}