public class OrderSearchEndpoint {

    private final java.sql.DataSource ds;

    public OrderSearchEndpoint(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public java.util.List<String> search(String sort, String dir) throws Exception {
        String sql = "SELECT id, customer FROM orders ORDER BY " + sort + " " + dir;

        java.util.ArrayList<String> out = new java.util.ArrayList<>();
        try (java.sql.Connection c = ds.getConnection();
             java.sql.Statement st = c.createStatement();
             java.sql.ResultSet rs = st.executeQuery(sql)) {

            while (rs.next()) {
                out.add(rs.getLong(1) + " " + rs.getString(2));
            }
        }
        return out;
    }
}