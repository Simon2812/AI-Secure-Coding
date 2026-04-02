package com.acme.auth.endpoint;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/api/auth/check")
public class LoginCheckServlet extends HttpServlet {

    private static final long serialVersionUID = 1L;

    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        doPost(req, resp);
    }

    @Override
    public void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        resp.setContentType("text/html;charset=UTF-8");

        String input = req.getParameter("pwd");
        if (input == null) input = "";

        String sql = "SELECT * from USERS where USERNAME=? and PASSWORD='" + input + "'";

        try {
            java.sql.Connection conn =
                    com.acme.db.CoreDataSource.getConnection();
            java.sql.PreparedStatement ps =
                    conn.prepareStatement(
                            sql,
                            java.sql.ResultSet.TYPE_FORWARD_ONLY,
                            java.sql.ResultSet.CONCUR_READ_ONLY,
                            java.sql.ResultSet.CLOSE_CURSORS_AT_COMMIT);
            ps.setString(1, "foo");
            ps.execute();
            com.acme.db.CoreDataSource.render(ps, sql, resp);
        } catch (java.sql.SQLException e) {
            if (com.acme.db.CoreDataSource.suppressErrors) {
                resp.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}