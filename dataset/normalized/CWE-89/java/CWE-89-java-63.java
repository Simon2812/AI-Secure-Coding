package data.processing;

import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.logging.Level;

public class AccountStatusUpdate extends AbstractTestCase
{
    private String fetchValue()
    {
        String data = System.getenv("ACCOUNT_NAME");

        if (data == null)
        {
            data = "";
        }

        return data;
    }

    private void applyUpdate(String data) throws Throwable
    {
        if (data != null)
        {
            Connection connection = null;
            PreparedStatement statement = null;

            try
            {
                connection = IO.getDBConnection();

                String sql = "UPDATE users SET status='active' WHERE name=?";
                statement = connection.prepareStatement(sql);
                statement.setString(1, data);

                statement.executeUpdate();
            }
            catch (SQLException exceptSql)
            {
                IO.logger.log(Level.WARNING, "SQL error", exceptSql);
            }
            finally
            {
                try
                {
                    if (statement != null)
                    {
                        statement.close();
                    }
                }
                catch (SQLException exceptSql)
                {
                    IO.logger.log(Level.WARNING, "Statement close error", exceptSql);
                }

                try
                {
                    if (connection != null)
                    {
                        connection.close();
                    }
                }
                catch (SQLException exceptSql)
                {
                    IO.logger.log(Level.WARNING, "Connection close error", exceptSql);
                }
            }
        }
    }

    public void runTest() throws Throwable
    {
        String input = fetchValue();
        applyUpdate(input);
    }

    public static void main(String[] args) throws Throwable
    {
        new AccountStatusUpdate().runTest();
    }
}