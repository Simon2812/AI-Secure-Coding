public class ProductCatalogService {

    public void fetchProducts(java.sql.Connection conn, String sort) throws Exception {
        String sql = "SELECT * FROM products ORDER BY " + sort;
        java.sql.Statement st = conn.createStatement();
        st.executeQuery(sql);
    }
}