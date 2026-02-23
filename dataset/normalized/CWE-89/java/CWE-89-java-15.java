package app.configsync;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.util.Properties;

import java.io.FileInputStream;
import java.io.IOException;

import java.util.logging.Level;

import java.sql.Connection;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class ConfigLookupTask extends AbstractTestCase {

    public void runTask() throws Throwable {

        String value = "";
        Properties props = new Properties();
        FileInputStream fis = null;

        try {
            fis = new FileInputStream("../common/config.properties");
            props.load(fis);
            value = props.getProperty("data");
        } catch (IOException e) {
            IO.logger.log(Level.WARNING, "Error with stream reading", e);
        } finally {
            try {
                if (fis != null) fis.close();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "Error closing FileInputStream", e);
            }
        }

        Connection conn = null;
        Statement st = null;
        ResultSet rs = null;

        try {
            conn = IO.getDBConnection();
            st = conn.createStatement();

            rs = st.executeQuery("select * from users where name='" + value + "'");

            int found = 0;
            while (rs.next()) {
                found++;
            }
            IO.writeLine("Found " + found + " record(s).");

        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Database error", e);
        } finally {

            try {
                if (rs != null) rs.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "ResultSet close error", e);
            }

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
        new ConfigLookupTask().runTask();
    }
}