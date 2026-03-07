package engine.exec;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.URL;
import java.net.URLConnection;

public class RemoteDirectoryTask {

    public void start() throws Exception {

        String input = "";

        URLConnection connection = new URL("http://www.example.org/").openConnection();
        BufferedReader reader = null;
        InputStreamReader stream = null;

        try {

            stream = new InputStreamReader(connection.getInputStream(), "UTF-8");
            reader = new BufferedReader(stream);

            input = reader.readLine();

        } catch (IOException e) {

            System.err.println("Network read failure: " + e.getMessage());

        } finally {

            try { if (reader != null) reader.close(); } catch (IOException ignored) {}
            try { if (stream != null) stream.close(); } catch (IOException ignored) {}

        }

        String tool;

        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            tool = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            tool = "/bin/ls ";
        }

        Process proc = Runtime.getRuntime().exec(tool + input);
        proc.waitFor();
    }

    public static void main(String[] args) throws Exception {
        new RemoteDirectoryTask().start();
    }
}