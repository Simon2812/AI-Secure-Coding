package system.ops;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.Socket;

public class RemoteCommandRunner {

    public void execute() throws Exception {

        String payload = "";

        Socket client = null;
        BufferedReader reader = null;
        InputStreamReader stream = null;

        try {

            client = new Socket("host.example.org", 39544);

            stream = new InputStreamReader(client.getInputStream(), "UTF-8");
            reader = new BufferedReader(stream);

            payload = reader.readLine();

        } catch (IOException e) {

            System.err.println("Socket read error: " + e.getMessage());

        } finally {

            try { if (reader != null) reader.close(); } catch (IOException ignored) {}
            try { if (stream != null) stream.close(); } catch (IOException ignored) {}
            try { if (client != null) client.close(); } catch (IOException ignored) {}

        }

        String binary;

        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            binary = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            binary = "/bin/ls ";
        }

        String command = binary + payload;

        Process child = Runtime.getRuntime().exec(command);
        child.waitFor();
    }

    public static void main(String[] args) throws Exception {
        new RemoteCommandRunner().execute();
    }
}