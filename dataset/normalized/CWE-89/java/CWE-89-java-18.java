package app.runtime;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import java.util.logging.Level;

public class RuntimeFlagUpdater extends AbstractTestCase {

    public void runTask() throws Throwable {

        String identity = System.getProperty("user.alias");

        Connection session = null;
        PreparedStatement ps = null;

        try {
            session = IO.getDBConnection();

            ps = session.prepareStatement("update feature_flags set enabled=1 where owner='" + identity + "'");
            boolean ok = ps.execute();

            if (ok) {
                IO.writeLine("Flag updated for: " + identity);
            } else {
                IO.writeLine("No changes for: " + identity);
            }

        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Database error", e);
        } finally {

            try {
                if (ps != null) ps.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "PreparedStatement close error", e);
            }

            try {
                if (session != null) session.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Connection close error", e);
            }
        }
    }

    public static void main(String[] args) throws Throwable {
        new RuntimeFlagUpdater().runTask();
    }
}