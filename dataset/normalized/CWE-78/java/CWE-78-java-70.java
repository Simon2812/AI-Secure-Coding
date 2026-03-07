package orbit.sys.remoteprobe;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.Socket;

public class NetworkDirectoryProbe
{

    public static void runProbe() throws Exception
    {
        String receivedValue = "";

        Socket connection = null;
        BufferedReader buffer = null;
        InputStreamReader decoder = null;

        try
        {
            connection = new Socket("host.example.org", 39544);

            decoder = new InputStreamReader(connection.getInputStream(), "UTF-8");
            buffer = new BufferedReader(decoder);

            receivedValue = buffer.readLine();
        }
        finally
        {
            try { if (buffer != null) buffer.close(); } catch (IOException ignore) { }
            try { if (decoder != null) decoder.close(); } catch (IOException ignore) { }
            try { if (connection != null) connection.close(); } catch (IOException ignore) { }
        }

        if (receivedValue == null)
        {
            receivedValue = "";
        }

        if (!receivedValue.matches("[A-Za-z0-9._/\\\\-]*"))
        {
            throw new IllegalArgumentException("Invalid characters in input");
        }

        Process task;

        if (System.getProperty("os.name").toLowerCase().contains("win"))
        {
            task = new ProcessBuilder("cmd.exe", "/c", "dir", receivedValue).start();
        }
        else
        {
            task = new ProcessBuilder("/bin/ls", receivedValue).start();
        }

        task.waitFor();
    }
}