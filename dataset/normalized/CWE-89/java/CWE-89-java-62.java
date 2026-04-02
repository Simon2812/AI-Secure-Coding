package core.logic;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import java.util.logging.Level;

public class EnvironmentUserSearch extends AbstractTestCase {

    private String readFromEnvironment() {
        String value = System.getenv("USER_QUERY");
        return value != null ? value : "";
    }

    private void performLookup(String value) {
        Connection connection = null;
        PreparedStatement statement = null;
        ResultSet resultSet = null;

        try {
            connection = IO.getDBConnection();
            statement = connection.prepareStatement(
                    "SELECT * FROM users WHERE name=?"
            );
            statement.setString(1, value);
            resultSet = statement.executeQuery();

            while (resultSet.next()) {
                IO.writeLine(resultSet.getString("name"));
            }

        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Database error", e);
        } finally {
            try {
                if (resultSet != null) resultSet.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Error closing ResultSet", e);
            }
            try {
                if (statement != null) statement.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Error closing PreparedStatement", e);
            }
            try {
                if (connection != null) connection.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Error closing Connection", e);
            }
        }
    }

    public void runTest() throws Throwable {
        String input = readFromEnvironment();
        performLookup(input);
    }

    public static void main(String[] args) throws Throwable {
        new EnvironmentUserSearch().runTest();
    }
}