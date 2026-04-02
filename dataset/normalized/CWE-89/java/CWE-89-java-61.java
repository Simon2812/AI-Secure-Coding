package app.service;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.Socket;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import java.util.logging.Level;

public class NetworkUserQuery extends AbstractTestCase {

    private String receiveData() {
        String data = "";
        Socket socket = null;
        BufferedReader reader = null;
        InputStreamReader streamReader = null;

        try {
            socket = new Socket("localhost", 39544);
            streamReader = new InputStreamReader(socket.getInputStream(), "UTF-8");
            reader = new BufferedReader(streamReader);
            data = reader.readLine();
        } catch (IOException e) {
            IO.logger.log(Level.WARNING, "I/O error", e);
        } finally {
            try {
                if (reader != null) reader.close();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "Error closing reader", e);
            }
            try {
                if (streamReader != null) streamReader.close();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "Error closing streamReader", e);
            }
            try {
                if (socket != null) socket.close();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "Error closing socket", e);
            }
        }

        return data;
    }

    private void executeQuery(String data) {
        Connection connection = null;
        PreparedStatement statement = null;
        ResultSet results = null;

        try {
            connection = IO.getDBConnection();
            statement = connection.prepareStatement(
                    "SELECT * FROM users WHERE name=?"
            );
            statement.setString(1, data);
            results = statement.executeQuery();

            while (results.next()) {
                IO.writeLine(results.getString("name"));
            }

        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Database error", e);
        } finally {
            try {
                if (results != null) results.close();
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
        String input = receiveData();
        executeQuery(input);
    }

    public static void main(String[] args) throws Throwable {
        new NetworkUserQuery().runTest();
    }
}