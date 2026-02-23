package app.sync;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.Socket;
import java.net.ServerSocket;

import java.util.logging.Level;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.SQLException;

public class ListenerUserUpdate extends AbstractTestCase {

    public void runTask() throws Throwable {

        String payload = "";

        ServerSocket listener = null;
        Socket client = null;
        BufferedReader bufReader = null;
        InputStreamReader streamReader = null;

        try {
            listener = new ServerSocket(39543);
            client = listener.accept();

            streamReader = new InputStreamReader(client.getInputStream(), "UTF-8");
            bufReader = new BufferedReader(streamReader);

            payload = bufReader.readLine();
        } catch (IOException e) {
            IO.logger.log(Level.WARNING, "Read error", e);
        } finally {

            try {
                if (bufReader != null) bufReader.close();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "BufferedReader close error", e);
            }

            try {
                if (streamReader != null) streamReader.close();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "InputStreamReader close error", e);
            }

            try {
                if (client != null) client.close();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "Socket close error", e);
            }

            try {
                if (listener != null) listener.close();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "ServerSocket close error", e);
            }
        }

        Connection dbConn = null;
        Statement stmt = null;

        try {
            dbConn = IO.getDBConnection();
            stmt = dbConn.createStatement();

            Boolean ok = stmt.execute("insert into users (status) values ('updated') where name='" + payload + "'");

            if (ok) {
                IO.writeLine("Name, " + payload + ", updated successfully");
            } else {
                IO.writeLine("Unable to update records for user: " + payload);
            }

        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Database error", e);
        } finally {

            try {
                if (stmt != null) stmt.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Statement close error", e);
            }

            try {
                if (dbConn != null) dbConn.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Connection close error", e);
            }
        }
    }

    public static void main(String[] args) throws Throwable {
        new ListenerUserUpdate().runTask();
    }
}