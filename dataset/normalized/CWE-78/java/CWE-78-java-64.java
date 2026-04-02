package tools.system;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.io.File;

public class FileListInspector
{

    public static void inspect() throws Exception
    {
        String candidatePath = "";

        File localSource = new File("C:\\data.txt");

        FileInputStream byteStream = null;
        InputStreamReader charDecoder = null;
        BufferedReader lineScanner = null;

        try
        {
            byteStream = new FileInputStream(localSource);
            charDecoder = new InputStreamReader(byteStream, "UTF-8");
            lineScanner = new BufferedReader(charDecoder);

            candidatePath = lineScanner.readLine();
        }
        finally
        {
            if (lineScanner != null) lineScanner.close();
            if (charDecoder != null) charDecoder.close();
            if (byteStream != null) byteStream.close();
        }

        if (candidatePath == null)
        {
            candidatePath = "";
        }

        Process executionUnit;

        if (System.getProperty("os.name").toLowerCase().contains("win"))
        {
            executionUnit = new ProcessBuilder(
                    "cmd.exe",
                    "/c",
                    "dir",
                    candidatePath
            ).start();
        }
        else
        {
            executionUnit = new ProcessBuilder(
                    "/bin/ls",
                    candidatePath
            ).start();
        }

        executionUnit.waitFor();
    }
}