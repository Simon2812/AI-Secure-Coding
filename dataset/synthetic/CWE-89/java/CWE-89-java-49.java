public class OrderQueryService {

    public void listRecentOrders(java.sql.Connection conn, String limit) throws Exception {
        String sql = "SELECT * FROM orders LIMIT " + limit;
        conn.createStatement().executeQuery(sql);
    }
}