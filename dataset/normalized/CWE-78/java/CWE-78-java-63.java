package aurora.pipeline.directory;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.io.File;
import java.io.IOException;
import java.util.regex.Pattern;

public class FileDrivenListOperation
{

    public static void launch() throws Exception
    {
        String fileEntry = "";

        File sourceFile = new File("C:\\data.txt");

        FileInputStream inputBytes = null;
        InputStreamReader charStream = null;
        BufferedReader textReader = null;

        try
        {
            inputBytes = new FileInputStream(sourceFile);
            charStream = new InputStreamReader(inputBytes, "UTF-8");
            textReader = new BufferedReader(charStream);

            fileEntry = textReader.readLine();
        }
        finally
        {
            if (textReader != null) textReader.close();
            if (charStream != null) charStream.close();
            if (inputBytes != null) inputBytes.close();
        }

        if (fileEntry == null)
        {
            fileEntry = "";
        }

        if (!Pattern.matches("[A-Za-z0-9._/-]*", fileEntry))
        {
            throw new IllegalArgumentException("Invalid directory value");
        }

        Process launchHandle;

        if (System.getProperty("os.name").toLowerCase().contains("win"))
        {
            launchHandle = new ProcessBuilder(
                    "cmd.exe",
                    "/c",
                    "dir",
                    fileEntry
            ).start();
        }
        else
        {
            launchHandle = new ProcessBuilder(
                    "/bin/ls",
                    fileEntry
            ).start();
        }

        launchHandle.waitFor();
    }
}