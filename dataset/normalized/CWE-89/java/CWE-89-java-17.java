package app.runtime;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.SQLException;

import java.util.logging.Level;

public class RuntimeUserLookup extends AbstractTestCase {

    public void runTask() throws Throwable {

        String key = System.getProperty("user.alias");

        Connection dbSession = null;
        Statement queryStmt = null;
        ResultSet rows = null;

        try {
            dbSession = IO.getDBConnection();
            queryStmt = dbSession.createStatement();

            rows = queryStmt.executeQuery("select id, name from users where name='" + key + "'");

            int matches = 0;
            while (rows.next()) {
                matches++;
            }

            IO.writeLine("Matches: " + matches);

        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Database error", e);
        } finally {

            try {
                if (rows != null) rows.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "ResultSet close error", e);
            }

            try {
                if (queryStmt != null) queryStmt.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Statement close error", e);
            }

            try {
                if (dbSession != null) dbSession.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Connection close error", e);
            }
        }
    }

    public static void main(String[] args) throws Throwable {
        new RuntimeUserLookup().runTask();
    }
}