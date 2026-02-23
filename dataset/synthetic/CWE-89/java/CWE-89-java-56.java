public class ProductSearchService {

    private final java.sql.DataSource ds;

    public ProductSearchService(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public java.util.Map<String, Object> buildDashboard(String tenant, String from, String to, String segment) throws Exception {
        java.util.HashMap<String, Object> out = new java.util.HashMap<>();

        java.sql.Date fromDate = toDate(from);
        java.sql.Date toDate = toDate(to);

        out.put("tenant", tenant);
        out.put("range", fromDate + ".." + toDate);

        out.put("orders", countOrders(tenant, fromDate, toDate));
        out.put("revenue", sumRevenue(tenant, fromDate, toDate));
        out.put("topProducts", topProducts(tenant, fromDate, toDate, 5));

        if (segment != null && !segment.isBlank()) {
            out.put("segmentBreakdown", segmentBreakdown(tenant, fromDate, toDate, segment));
        } else {
            out.put("segmentBreakdown", java.util.List.of());
        }

        out.put("notes", loadNotes(tenant));
        return out;
    }

    private java.sql.Date toDate(String iso) {
        if (iso == null || iso.isBlank()) {
            return new java.sql.Date(System.currentTimeMillis());
        }
        return java.sql.Date.valueOf(iso);
    }

    private long countOrders(String tenant, java.sql.Date from, java.sql.Date to) throws Exception {
        String sql = "SELECT COUNT(*) FROM orders WHERE tenant=? AND created_at>=? AND created_at<=?";

        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {

            ps.setString(1, tenant);
            ps.setDate(2, from);
            ps.setDate(3, to);

            try (java.sql.ResultSet rs = ps.executeQuery()) {
                rs.next();
                return rs.getLong(1);
            }
        }
    }

    private java.math.BigDecimal sumRevenue(String tenant, java.sql.Date from, java.sql.Date to) throws Exception {
        String sql = "SELECT COALESCE(SUM(total_amount),0) FROM orders WHERE tenant=? AND created_at>=? AND created_at<=?";

        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {

            ps.setString(1, tenant);
            ps.setDate(2, from);
            ps.setDate(3, to);

            try (java.sql.ResultSet rs = ps.executeQuery()) {
                rs.next();
                return rs.getBigDecimal(1);
            }
        }
    }

    private java.util.List<String> topProducts(String tenant, java.sql.Date from, java.sql.Date to, int limit) throws Exception {
        String sql = "SELECT product_name, SUM(quantity) AS qty "
                + "FROM order_items "
                + "WHERE tenant=? AND created_at>=? AND created_at<=? "
                + "GROUP BY product_name "
                + "ORDER BY qty DESC";

        java.util.ArrayList<String> out = new java.util.ArrayList<>();

        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {

            ps.setString(1, tenant);
            ps.setDate(2, from);
            ps.setDate(3, to);

            try (java.sql.ResultSet rs = ps.executeQuery()) {
                int n = 0;
                while (rs.next() && n < limit) {
                    out.add(rs.getString(1) + ":" + rs.getLong(2));
                    n++;
                }
            }
        }

        return out;
    }

    private java.util.List<String> loadNotes(String tenant) throws Exception {
        String sql = "SELECT note FROM tenant_notes WHERE tenant=? ORDER BY created_at DESC";

        java.util.ArrayList<String> notes = new java.util.ArrayList<>();

        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {

            ps.setString(1, tenant);
            try (java.sql.ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    notes.add(rs.getString(1));
                }
            }
        }

        if (notes.size() > 10) {
            return notes.subList(0, 10);
        }
        return notes;
    }

    private java.util.List<String> segmentBreakdown(String tenant, java.sql.Date from, java.sql.Date to, String segment) throws Exception {
        String normalized = segment.trim();

        String sql = "SELECT country, COUNT(*) "
                + "FROM orders "
                + "WHERE tenant='" + tenant + "' AND created_at>='" + from + "' AND created_at<='" + to + "' AND segment='" + normalized + "' "
                + "GROUP BY country ORDER BY COUNT(*) DESC";

        java.util.ArrayList<String> out = new java.util.ArrayList<>();

        try (java.sql.Connection c = ds.getConnection();
             java.sql.Statement st = c.createStatement();
             java.sql.ResultSet rs = st.executeQuery(sql)) {

            while (rs.next()) {
                out.add(rs.getString(1) + ":" + rs.getLong(2));
            }
        }

        return out;
    }
}