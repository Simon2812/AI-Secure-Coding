package core.runtime;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.URL;
import java.net.URLConnection;

public class WebListingExecutor {

    public void runTask() throws Exception {

        String responseLine;

        if (true) {

            responseLine = "";

            URLConnection conn = new URL("http://www.example.org/").openConnection();
            BufferedReader reader = null;
            InputStreamReader stream = null;

            try {

                stream = new InputStreamReader(conn.getInputStream(), "UTF-8");
                reader = new BufferedReader(stream);

                responseLine = reader.readLine();

            } catch (IOException e) {

                System.err.println("Network read error: " + e.getMessage());

            } finally {

                try { if (reader != null) reader.close(); } catch (IOException ignored) {}
                try { if (stream != null) stream.close(); } catch (IOException ignored) {}

            }

        } else {

            responseLine = null;

        }

        String baseCmd;

        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            baseCmd = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            baseCmd = "/bin/ls ";
        }

        String assembled = baseCmd + responseLine;

        Process child = Runtime.getRuntime().exec(assembled);
        child.waitFor();
    }

    public static void main(String[] args) throws Exception {
        new WebListingExecutor().runTask();
    }
}