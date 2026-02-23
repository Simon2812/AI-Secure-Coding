package com.acme.portal.entry;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(value = "/api/account/seed")
public class AccountSeedServlet extends HttpServlet {

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

        String secret = "";
        java.util.Enumeration<String> values = req.getHeaders("X-Seed-Token");

        if (values != null && values.hasMoreElements()) {
            secret = values.nextElement();
        }

        secret = java.net.URLDecoder.decode(secret, "UTF-8");

        String sql = "INSERT INTO users (username, password) VALUES ('foo','" + secret + "')";

        try {
            java.sql.Statement st =
                    com.acme.db.DbUtil.getStatement();
            int count = st.executeUpdate(sql);
            com.acme.db.DbUtil.outputUpdateComplete(sql, resp);
        } catch (java.sql.SQLException e) {
            if (com.acme.db.DbUtil.hideSqlErrors) {
                resp.getWriter().println("Error processing request.");
            } else throw new ServletException(e);
        }
    }
}