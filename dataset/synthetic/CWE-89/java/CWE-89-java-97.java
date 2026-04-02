public class ExportPolicyChecker {

    private final java.sql.DataSource ds;

    public ExportPolicyChecker(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public boolean canExport(String actorId, String accountId) throws Exception {
        if (actorId == null || accountId == null) return false;

        try (java.sql.Connection c = ds.getConnection()) {
            String role = loadRole(c, actorId);
            if (!"admin".equalsIgnoreCase(role) && !"finance".equalsIgnoreCase(role)) {
                return false;
            }
            return accountHasInvoices(c, accountId);
        }
    }

    private String loadRole(java.sql.Connection c, String actorId) throws Exception {
        String sql = "SELECT role FROM operators WHERE id=?";
        try (java.sql.PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, actorId);
            try (java.sql.ResultSet rs = ps.executeQuery()) {
                return rs.next() ? rs.getString(1) : "";
            }
        }
    }

    private boolean accountHasInvoices(java.sql.Connection c, String accountId) throws Exception {
        String sql = "SELECT 1 FROM invoices WHERE account_id=?";
        try (java.sql.PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, accountId);
            try (java.sql.ResultSet rs = ps.executeQuery()) {
                return rs.next();
            }
        }
    }
}