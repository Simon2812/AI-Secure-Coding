package dataset.normalized.cwe78;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.Socket;
import java.net.ServerSocket;

public class NetworkDirectoryExecutor
{

    public static void runTask() throws Exception
    {
        String clientValue = "";

        ServerSocket socketServer = null;
        Socket clientSocket = null;
        BufferedReader networkReader = null;
        InputStreamReader byteReader = null;

        try
        {
            socketServer = new ServerSocket(39543);
            clientSocket = socketServer.accept();

            byteReader = new InputStreamReader(clientSocket.getInputStream(), "UTF-8");
            networkReader = new BufferedReader(byteReader);

            clientValue = networkReader.readLine();
        }
        catch (IOException io)
        {
            throw new RuntimeException(io);
        }
        finally
        {
            if (networkReader != null) networkReader.close();
            if (byteReader != null) byteReader.close();
            if (clientSocket != null) clientSocket.close();
            if (socketServer != null) socketServer.close();
        }

        String baseCmd;

        if (System.getProperty("os.name").toLowerCase().indexOf("win") >= 0)
        {
            baseCmd = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        }
        else
        {
            baseCmd = "/bin/ls ";
        }

        Process execProcess = Runtime.getRuntime().exec(baseCmd + clientValue);
        execProcess.waitFor();
    }
}