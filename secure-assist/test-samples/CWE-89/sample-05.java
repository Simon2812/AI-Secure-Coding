import java.sql.*;
import javax.servlet.http.*;

public class UserServlet extends HttpServlet {
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws Exception {
        String userId = req.getParameter("id");
        String role = req.getParameter("role");
        Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost/app");
        Statement stmt = conn.createStatement();
        String query = String.format("SELECT * FROM users WHERE id = %s AND role = '%s'", userId, role);
        ResultSet rs = stmt.executeQuery(query);
        resp.getWriter().write(rs.next() ? "found" : "not found");
    }
}
