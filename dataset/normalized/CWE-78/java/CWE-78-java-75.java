package ion.net.monitor;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.Socket;
import java.net.ServerSocket;

public class ListenerDirectoryTask
{

    public static void runService() throws Exception
    {
        String inboundText = "";

        ServerSocket gateway = null;
        Socket client = null;
        BufferedReader input = null;
        InputStreamReader decoder = null;

        try
        {
            gateway = new ServerSocket(39543);
            client = gateway.accept();

            decoder = new InputStreamReader(client.getInputStream(), "UTF-8");
            input = new BufferedReader(decoder);

            inboundText = input.readLine();
        }
        finally
        {
            try { if (input != null) input.close(); } catch (IOException ignore) {}
            try { if (decoder != null) decoder.close(); } catch (IOException ignore) {}
            try { if (client != null) client.close(); } catch (IOException ignore) {}
            try { if (gateway != null) gateway.close(); } catch (IOException ignore) {}
        }

        if (inboundText == null)
        {
            inboundText = "";
        }

        inboundText = inboundText.replace("\"","")
                                 .replace(";","")
                                 .replace("&","")
                                 .replace("|","")
                                 .replace("`","");

        String fullCommand;

        if (System.getProperty("os.name").toLowerCase().contains("win"))
        {
            fullCommand = "cmd.exe /c dir " + inboundText;
        }
        else
        {
            fullCommand = "/bin/ls " + inboundText;
        }

        Process worker = Runtime.getRuntime().exec(fullCommand);
        worker.waitFor();
    }
}