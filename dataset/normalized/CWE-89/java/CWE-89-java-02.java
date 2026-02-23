package app.sync;

import juliet.support.IO;
import juliet.support.AbstractTestCase;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.SQLException;

import java.util.logging.Level;

public class RemoteUpdater extends AbstractTestCase {

    public void execute() throws Throwable {

        String received = "";

        Socket socket = null;
        BufferedReader reader = null;

        try {
            socket = new Socket("host.example.org", 39544);
            reader = new BufferedReader(new InputStreamReader(socket.getInputStream(), "UTF-8"));
            received = reader.readLine();
        } catch (Exception e) {
            IO.logger.log(Level.WARNING, "Network read error", e);
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

        if (received != null) {

            String[] users = received.split(",");
            int count = 0;

            Connection connection = null;
            Statement statement = null;

            try {
                connection = IO.getDBConnection();
                statement = connection.createStatement();

                for (int i = 0; i < users.length; i++) {
                    statement.addBatch("update users set role='member' where username='" + users[i] + "'");
                }

                int[] results = statement.executeBatch();

                for (int i = 0; i < results.length; i++) {
                    if (results[i] > 0) {
                        count++;
                    }
                }

                IO.writeLine("Processed " + count + " entries.");

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
        new RemoteUpdater().execute();
    }
}