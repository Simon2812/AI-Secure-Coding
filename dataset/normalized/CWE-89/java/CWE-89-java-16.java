package app.settings;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.util.Properties;

import java.io.FileInputStream;
import java.io.IOException;

import java.util.logging.Level;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class SettingsWriterTask extends AbstractTestCase {

    public void runTask() throws Throwable {

        Properties settings = new Properties();
        String principal = "";
        FileInputStream propIn = null;

        try {
            propIn = new FileInputStream("../common/config.properties");
            settings.load(propIn);
            principal = settings.getProperty("data");
        } catch (IOException e) {
            IO.logger.log(Level.WARNING, "Config read error", e);
        } finally {
            try {
                if (propIn != null) propIn.close();
            } catch (IOException e) {
                IO.logger.log(Level.WARNING, "Stream close error", e);
            }
        }

        Connection dbLink = null;
        PreparedStatement ps = null;

        try {
            dbLink = IO.getDBConnection();

            ps = dbLink.prepareStatement("update user_settings set enabled=1 where username='" + principal + "'");
            boolean ok = ps.execute();

            if (ok) {
                IO.writeLine("Updated settings for: " + principal);
            } else {
                IO.writeLine("No update performed for: " + principal);
            }

        } catch (SQLException e) {
            IO.logger.log(Level.WARNING, "Database error", e);
        } finally {

            try {
                if (ps != null) ps.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "PreparedStatement close error", e);
            }

            try {
                if (dbLink != null) dbLink.close();
            } catch (SQLException e) {
                IO.logger.log(Level.WARNING, "Connection close error", e);
            }
        }
    }

    public static void main(String[] args) throws Throwable {
        new SettingsWriterTask().runTask();
    }
}