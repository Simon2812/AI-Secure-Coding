package app.records;

import juliet.support.IO;
import juliet.support.AbstractTestCase;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.SQLException;
import java.util.logging.Level;

public class UserHitUpdater extends AbstractTestCase {

    public void process() throws Throwable {

        String input = System.getenv("ADD");

        if (input != null) {

            String[] entries = input.split("-");
            int updated = 0;

            Connection connection = null;
            Statement statement = null;

            try {
                connection = IO.getDBConnection();
                statement = connection.createStatement();

                for (int i = 0; i < entries.length; i++) {
                    statement.addBatch("update users set hitcount=hitcount+1 where name='" + entries[i] + "'");
                }

                int[] results = statement.executeBatch();

                for (int i = 0; i < results.length; i++) {
                    if (results[i] > 0) {
                        updated++;
                    }
                }

                IO.writeLine("Updated " + updated + " of " + entries.length + " records.");

            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Database error", e);
            } finally {

                try {
                    if (statement != null) {
                        statement.close();
                    }
                } catch (SQLException e) {
                    IO.logger.log(Level.WARNING, "Statement close error", e);
                }

                try {
                    if (connection != null) {
                        connection.close();
                    }
                } catch (SQLException e) {
                    IO.logger.log(Level.WARNING, "Connection close error", e);
                }
            }
        }
    }

    public static void main(String[] args) throws Throwable {
        new UserHitUpdater().process();
    }
}
