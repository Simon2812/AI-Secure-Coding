package app.configsync;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.util.Properties;

import java.io.FileInputStream;
import java.io.IOException;

import java.util.logging.Level;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.SQLException;

public class ConfigBasedUpdater extends AbstractTestCase {

    public void runTask() throws Throwable {

        String data = "";
        Properties cfg = new Properties();
        FileInputStream fis = null;

        try {
            fis = new FileInputStream("../common/config.properties");
            cfg.load(fis);
            data = cfg.getProperty("data");
        } catch (IOException e) {
            IO.logger.log(Level.WARNING, "Error with stream reading", e);
        } finally {
            try {
                if (fis != null) {
                    fis.close();
                }
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "Error closing FileInputStream", e);
            }
        }

        Connection conn = null;
        Statement st = null;

        try {
            conn = IO.getDBConnection();
            st = conn.createStatement();

            Boolean result = st.execute("insert into users (status) values ('updated') where name='" + data + "'");

            if (result) {
                IO.writeLine("Name, " + data + ", updated successfully");
            } else {
                IO.writeLine("Unable to update records for user: " + data);
            }

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
        new ConfigBasedUpdater().runTask();
    }
}