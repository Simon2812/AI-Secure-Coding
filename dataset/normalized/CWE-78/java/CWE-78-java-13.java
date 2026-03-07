package network.utility;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.Socket;

public class RemoteDirectoryProbe {

    private static final boolean USE_REMOTE_INPUT = true;
    private static final boolean UNUSED_PATH = false;

    public void execute() throws Exception {

        String remoteValue;

        if (USE_REMOTE_INPUT) {

            remoteValue = "";

            Socket connection = null;
            BufferedReader reader = null;
            InputStreamReader stream = null;

            try {

                connection = new Socket("host.example.org", 39544);
                stream = new InputStreamReader(connection.getInputStream(), "UTF-8");
                reader = new BufferedReader(stream);

                remoteValue = reader.readLine();

            } catch (IOException e) {

                System.err.println("Network read failure: " + e.getMessage());

            } finally {

                try { if (reader != null) reader.close(); } catch (IOException ignored) {}
                try { if (stream != null) stream.close(); } catch (IOException ignored) {}
                try { if (connection != null) connection.close(); } catch (IOException ignored) {}
            }

        } else {

            remoteValue = null;
        }

        String command;

        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            command = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            command = "/bin/ls ";
        }

        Process proc = Runtime.getRuntime().exec(command + remoteValue);
        proc.waitFor();
    }

    public static void main(String[] args) throws Exception {
        new RemoteDirectoryProbe().execute();
    }
}