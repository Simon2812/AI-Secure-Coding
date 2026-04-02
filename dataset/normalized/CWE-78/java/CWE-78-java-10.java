package stream.gateway.exec;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.Socket;
import java.net.ServerSocket;

public class TcpDirectoryService {

    public void handle() throws Exception {

        String data;
        data = "";

        ServerSocket listener = null;
        Socket socket = null;
        BufferedReader readerBuffered = null;
        InputStreamReader readerInputStream = null;

        try {
            listener = new ServerSocket(39543);
            socket = listener.accept();

            readerInputStream = new InputStreamReader(socket.getInputStream(), "UTF-8");
            readerBuffered = new BufferedReader(readerInputStream);

            data = readerBuffered.readLine();

        } finally {

            try { if (readerBuffered != null) readerBuffered.close(); } catch (IOException ignored) {}
            try { if (readerInputStream != null) readerInputStream.close(); } catch (IOException ignored) {}
            try { if (socket != null) socket.close(); } catch (IOException ignored) {}
            try { if (listener != null) listener.close(); } catch (IOException ignored) {}
        }

        String osCommand;

        if(System.getProperty("os.name").toLowerCase().indexOf("win") >= 0) {
            osCommand = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir";
        } else {
            osCommand = "/bin/ls";
        }

        String[] command = osCommand.trim().split("\\s+");
        String[] full = new String[command.length + 1];
        System.arraycopy(command, 0, full, 0, command.length);
        full[command.length] = data;

        Process process = Runtime.getRuntime().exec(full);
        process.waitFor();
    }

    public static void main(String[] args) throws Exception {
        new TcpDirectoryService().handle();
    }
}