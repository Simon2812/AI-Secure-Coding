public class PostSearchService {

    public void searchPosts(java.sql.Connection conn, String term) throws Exception {
        String sql = "SELECT * FROM posts WHERE title LIKE '%" + term + "%'";
        java.sql.Statement st = conn.createStatement();
        st.executeQuery(sql);
    }
}