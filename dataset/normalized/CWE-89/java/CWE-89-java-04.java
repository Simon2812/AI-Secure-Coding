package app.tasks;

import juliet.support.IO;
import juliet.support.AbstractTestCase;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import java.util.logging.Level;

public class ProfileLookup extends AbstractTestCase {

    public void execute() throws Throwable {

        String input = System.getenv("USER_NAME");

        if (input != null) {

            Connection connection = null;
            PreparedStatement statement = null;

            try {
                connection = IO.getDBConnection();

                String query = "select * from profiles where username='" + input + "'";
                statement = connection.prepareStatement(query);

                statement.executeQuery();

            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Database error", e);
            } finally {

                try {
                    if (statement != null) statement.close();
                } catch (SQLException e) {
                    IO.logger.log(Level.WARNING, "Statement close error", e);
                }

                try {
                    if (connection != null) connection.close();
                } catch (SQLException e) {
                    IO.logger.log(Level.WARNING, "Connection close error", e);
                }
            }
        }
    }

    public static void main(String[] args) throws Throwable {
        new ProfileLookup().execute();
    }
}