package system.tools;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class DirectoryConsoleUtility {

    private static final boolean USE_CONSOLE = true;
    private static final boolean UNUSED_BRANCH = false;

    public void run() throws Exception {

        String argument;

        if (USE_CONSOLE) {

            argument = "";

            InputStreamReader input = null;
            BufferedReader buffer = null;

            try {

                input = new InputStreamReader(System.in, "UTF-8");
                buffer = new BufferedReader(input);

                argument = buffer.readLine();

            } catch (IOException e) {

                System.err.println("Input error: " + e.getMessage());

            } finally {

                try { if (buffer != null) buffer.close(); } catch (IOException ignored) {}
                try { if (input != null) input.close(); } catch (IOException ignored) {}
            }

        } else {

            argument = null;
        }

        String commandPrefix;

        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            commandPrefix = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            commandPrefix = "/bin/ls ";
        }

        Process p = Runtime.getRuntime().exec(commandPrefix + argument);
        p.waitFor();
    }

    public static void main(String[] args) throws Exception {
        new DirectoryConsoleUtility().run();
    }
}