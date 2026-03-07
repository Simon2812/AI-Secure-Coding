package atlas.shell.viewer;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class TerminalDirectoryViewer
{

    public static void launch() throws Exception
    {
        String userInput = "";

        BufferedReader consoleReader = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));

        userInput = consoleReader.readLine();

        if (userInput == null)
        {
            userInput = "";
        }

        if (!userInput.matches("[A-Za-z0-9._/\\\\-]*"))
        {
            throw new IllegalArgumentException("Unexpected characters");
        }

        Process worker;

        if (System.getProperty("os.name").toLowerCase().contains("win"))
        {
            worker = new ProcessBuilder("cmd.exe", "/c", "dir", userInput).start();
        }
        else
        {
            worker = new ProcessBuilder("/bin/ls", userInput).start();
        }

        worker.waitFor();
    }
}