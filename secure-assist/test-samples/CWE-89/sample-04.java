import java.sql.*;
import javax.servlet.http.*;

public class SearchServlet extends HttpServlet {
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws Exception {
        String keyword = req.getParameter("q");
        Connection conn = DriverManager.getConnection("jdbc:mysql://localhost/db", "user", "pass");
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("SELECT * FROM articles WHERE title LIKE '%" + keyword + "%'");
        StringBuilder sb = new StringBuilder();
        while (rs.next()) sb.append(rs.getString("title")).append("\n");
        resp.getWriter().write(sb.toString());
    }
}
