public class TenantMetricsReporter {

    private final java.sql.DataSource ds;

    public TenantMetricsReporter(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public long count(String tenant, String from, String to) throws Exception {
        if (tenant == null) return 0;

        String sql = "SELECT COUNT(*) FROM events WHERE tenant='" + tenant + "' AND event_day>=? AND event_day<=?";

        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {

            ps.setDate(1, java.sql.Date.valueOf(from));
            ps.setDate(2, java.sql.Date.valueOf(to));

            try (java.sql.ResultSet rs = ps.executeQuery()) {
                rs.next();
                return rs.getLong(1);
            }
        }
    }
}