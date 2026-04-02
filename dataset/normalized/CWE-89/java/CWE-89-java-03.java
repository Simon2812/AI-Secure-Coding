package app.sync;

import juliet.support.IO;
import juliet.support.AbstractTestCase;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.Socket;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.SQLException;

import java.util.logging.Level;

public class AccountUpdater extends AbstractTestCase {

    public void runTask() throws Throwable {

        String data = "";

        Socket socket = null;
        BufferedReader reader = null;

        try {
            socket = new Socket("host.example.org", 39544);
            reader = new BufferedReader(new InputStreamReader(socket.getInputStream(), "UTF-8"));
            data = reader.readLine();
        } catch (Exception e) {
            IO.logger.log(Level.WARNING, "Network error", e);
        } finally {
            try {
                if (reader != null) reader.close();
            } catch (Exception e) {
                IO.logger.log(Level.WARNING, "Reader close error", e);
            }
            try {
                if (socket != null) socket.close();
            } catch (Exception e) {
                IO.logger.log(Level.WARNING, "Socket close error", e);
            }
        }

        if (data != null) {

            Connection connection = null;
            Statement statement = null;

            try {
                connection = IO.getDBConnection();
                statement = connection.createStatement();

                statement.executeUpdate("update accounts set status='active' where username='" + data + "'");

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
        new AccountUpdater().runTask();
    }
}