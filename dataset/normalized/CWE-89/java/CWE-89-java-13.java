package app.sync;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

import java.net.ServerSocket;
import java.net.Socket;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.SQLException;

import java.util.logging.Level;

public class ListenerUserUpdater extends AbstractTestCase {

    public void runTask() throws Throwable {

        String requestLine = "";

        ServerSocket server = null;
        Socket client = null;
        InputStreamReader stream = null;
        BufferedReader reader = null;

        try {
            server = new ServerSocket(39543);
            client = server.accept();

            stream = new InputStreamReader(client.getInputStream(), "UTF-8");
            reader = new BufferedReader(stream);

            requestLine = reader.readLine();
        } catch (IOException e) {
            IO.logger.log(Level.WARNING, "Socket read error", e);
        } finally {

            try {
                if (reader != null) reader.close();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "Reader close error", e);
            }

            try {
                if (stream != null) stream.close();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "Stream close error", e);
            }

            try {
                if (client != null) client.close();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "Client close error", e);
            }

            try {
                if (server != null) server.close();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "Server close error", e);
            }
        }

        Connection conn = null;
        Statement st = null;

        try {
            conn = IO.getDBConnection();
            st = conn.createStatement();

            int rowCount = st.executeUpdate("insert into users (status) values ('updated') where name='" + requestLine + "'");

            IO.writeLine("Updated " + rowCount + " rows successfully.");
        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Database error", e);
        } finally {

            try {
                if (st != null) st.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Statement close error", e);
            }

            try {
                if (conn != null) conn.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Connection close error", e);
            }
        }
    }

    public static void main(String[] args) throws Throwable {
        new ListenerUserUpdater().runTask();
    }
}