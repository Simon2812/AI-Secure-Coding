package app.ingest;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import java.util.logging.Level;

public class FileDrivenFlagUpdate extends AbstractTestCase {

    public void runTask() throws Throwable {

        String identifier = "";
        BufferedReader fileReader = null;

        try {
            fileReader = new BufferedReader(new FileReader("input.txt"));
            identifier = fileReader.readLine();
        } catch (IOException e) {
            IO.logger.log(Level.WARNING, "File read error", e);
        } finally {
            try {
                if (fileReader != null) {
                    fileReader.close();
                }
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "Reader close error", e);
            }
        }

        Connection connectionHandle = null;
        PreparedStatement updateStmt = null;

        try {
            connectionHandle = IO.getDBConnection();

            updateStmt = connectionHandle.prepareStatement(
                "update audit_events set processed=1 where actor='" + identifier + "'"
            );

            boolean result = updateStmt.execute();

            if (result) {
                IO.writeLine("Processed events for: " + identifier);
            } else {
                IO.writeLine("No events updated for: " + identifier);
            }

        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Database error", e);
        } finally {

            try {
                if (updateStmt != null) {
                    updateStmt.close();
                }
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "PreparedStatement close error", e);
            }

            try {
                if (connectionHandle != null) {
                    connectionHandle.close();
                }
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Connection close error", e);
            }
        }
    }

    public static void main(String[] args) throws Throwable {
        new FileDrivenFlagUpdate().runTask();
    }
}