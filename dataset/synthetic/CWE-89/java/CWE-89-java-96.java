public class MetricLoader {

    private final java.sql.DataSource ds;

    public MetricLoader(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public java.util.Map<String, Object> load(String type, int page, int size) throws Exception {
        if (page < 0) page = 0;
        if (size < 1) size = 20;
        if (size > 100) size = 100;

        QueryType qt = QueryType.from(type);

        java.util.HashMap<String, Object> out = new java.util.HashMap<>();
        out.put("type", qt.name());
        out.put("page", page);
        out.put("size", size);

        try (java.sql.Connection c = ds.getConnection()) {
            long total = count(c, qt);
            java.util.List<String> rows = fetchPage(c, qt, page, size);

            out.put("total", total);
            out.put("rows", rows);
        }

        return out;
    }

    private long count(java.sql.Connection c, QueryType qt) throws Exception {
        String sql = "SELECT COUNT(*) FROM " + qt.table;
        try (java.sql.Statement st = c.createStatement();
             java.sql.ResultSet rs = st.executeQuery(sql)) {
            rs.next();
            return rs.getLong(1);
        }
    }

    private java.util.List<String> fetchPage(java.sql.Connection c, QueryType qt, int page, int size) throws Exception {
        String sql = "SELECT " + qt.column + " FROM " + qt.table + " ORDER BY " + qt.column + " ASC LIMIT " + size + " OFFSET " + (page * size);

        java.util.ArrayList<String> out = new java.util.ArrayList<>();

        try (java.sql.Statement st = c.createStatement();
             java.sql.ResultSet rs = st.executeQuery(sql)) {

            while (rs.next()) {
                out.add(rs.getString(1));
            }
        }

        return out;
    }

    private enum QueryType {
        USERS("users", "username"),
        TEAMS("teams", "name"),
        PRODUCTS("products", "product_name");

        final String table;
        final String column;

        QueryType(String table, String column) {
            this.table = table;
            this.column = column;
        }

        static QueryType from(String input) {
            if (input == null) return USERS;
            return switch (input) {
                case "teams" -> TEAMS;
                case "products" -> PRODUCTS;
                default -> USERS;
            };
        }
    }
}