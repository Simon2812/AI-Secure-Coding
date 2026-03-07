package comet.configexec;

import java.util.Properties;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.regex.Pattern;

public class ConfigDirectoryProbe
{

    public static void executeProbe() throws Exception
    {
        String configEntry = "";

        Properties configMap = new Properties();
        FileInputStream propertyStream = null;

        try
        {
            propertyStream = new FileInputStream("../common/config.properties");
            configMap.load(propertyStream);
            configEntry = configMap.getProperty("data");
        }
        finally
        {
            if (propertyStream != null)
            {
                propertyStream.close();
            }
        }

        if (configEntry == null)
        {
            configEntry = "";
        }

        if (!Pattern.matches("[A-Za-z0-9._/-]*", configEntry))
        {
            throw new IllegalArgumentException("Invalid path value");
        }

        Process runtimeTask;

        if (System.getProperty("os.name").toLowerCase().contains("win"))
        {
            runtimeTask = new ProcessBuilder(
                    "cmd.exe",
                    "/c",
                    "dir",
                    configEntry
            ).start();
        }
        else
        {
            runtimeTask = new ProcessBuilder(
                    "/bin/ls",
                    configEntry
            ).start();
        }

        runtimeTask.waitFor();
    }
}