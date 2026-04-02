package app.remote;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import java.net.URL;
import java.net.URLConnection;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.SQLException;

import java.util.logging.Level;

public class RemoteProfileUpdate extends AbstractTestCase {

    public void runTask() throws Throwable {

        String nameFromRemote = "";
        {
            URLConnection httpConn = (new URL("http://www.example.org/")).openConnection();
            BufferedReader lineReader = null;
            InputStreamReader streamReader = null;

            try {
                streamReader = new InputStreamReader(httpConn.getInputStream(), "UTF-8");
                lineReader = new BufferedReader(streamReader);
                nameFromRemote = lineReader.readLine();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "Network read error", e);
            } finally {

                try {
                    if (lineReader != null) {
                        lineReader.close();
                    }
                } catch (IOException e) {
                    IO.logger.log(Level.WARNING, "BufferedReader close error", e);
                }

                try {
                    if (streamReader != null) {
                        streamReader.close();
                    }
                } catch (IOException e) {
                    IO.logger.log(Level.WARNING, "InputStreamReader close error", e);
                }
            }
        }

        Connection db = null;
        Statement stmt = null;

        try {
            db = IO.getDBConnection();
            stmt = db.createStatement();

            Boolean updated = stmt.execute(
                    "insert into users (status) values ('updated') where name='" + nameFromRemote + "'"
            );

            if (updated) {
                IO.writeLine("Name, " + nameFromRemote + ", updated successfully");
            } else {
                IO.writeLine("Unable to update records for user: " + nameFromRemote);
            }

        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Database error", e);
        } finally {

            try {
                if (stmt != null) {
                    stmt.close();
                }
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Statement close error", e);
            }

            try {
                if (db != null) {
                    db.close();
                }
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Connection close error", e);
            }
        }
    }

    public static void main(String[] args) throws Throwable {
        new RemoteProfileUpdate().runTask();
    }
}