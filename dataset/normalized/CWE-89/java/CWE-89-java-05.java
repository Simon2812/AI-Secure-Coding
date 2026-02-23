package app.imports;

import juliet.support.IO;
import juliet.support.AbstractTestCase;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.SQLException;

import java.util.logging.Level;

public class BatchExecutor extends AbstractTestCase {

    public void perform() throws Throwable {

        String content = "";

        File file = new File("input.txt");
        BufferedReader reader = null;

        try {
            reader = new BufferedReader(new FileReader(file));
            content = reader.readLine();
        } catch (IOException e) {
            IO.logger.log(Level.WARNING, "File read error", e);
        } finally {
            try {
                if (reader != null) reader.close();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "Reader close error", e);
            }
        }

        if (content != null) {

            Connection connection = null;
            Statement statement = null;

            try {
                connection = IO.getDBConnection();
                statement = connection.createStatement();

                statement.execute("delete from logs where category='" + content + "'");

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
        new BatchExecutor().perform();
    }
}