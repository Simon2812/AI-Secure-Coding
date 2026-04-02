package web.controllers;

import juliet.support.IO;
import juliet.support.AbstractTestCaseServlet;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.SQLException;

import java.util.logging.Level;

public class ProductLookupServlet extends AbstractTestCaseServlet {

    public void doGet(HttpServletRequest request, HttpServletResponse response) throws Throwable {

        String rawQuery = request.getQueryString();

        Connection dbConnection = null;
        Statement sqlStatement = null;
        ResultSet results = null;

        try {
            dbConnection = IO.getDBConnection();
            sqlStatement = dbConnection.createStatement();

            results = sqlStatement.executeQuery("select * from products where code='" + rawQuery + "'");

            int total = 0;
            while (results.next()) {
                total++;
            }

            response.getWriter().println("Matches: " + total);

        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Query execution error", e);
        } catch (Exception e) {
            IO.logger.log(Level.WARNING, "Response error", e);
        } finally {

            try {
                if (results != null) results.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "ResultSet close error", e);
            }

            try {
                if (sqlStatement != null) sqlStatement.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Statement close error", e);
            }

            try {
                if (dbConnection != null) dbConnection.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Connection close error", e);
            }
        }
    }
}