import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

public class TraceService {

    public static void main(String[] args) throws IOException {

        ServerSocket server = new ServerSocket(9090);
        System.out.println("Trace service listening on port 9090");

        Socket client = server.accept();
        BufferedReader reader = new BufferedReader(new InputStreamReader(client.getInputStream()));

        String destination = reader.readLine();

        String cmd = "traceroute " + destination;

        Process process = Runtime.getRuntime().exec(cmd);

        System.out.println("Tracing route to " + destination);

        reader.close();
        client.close();
        server.close();
    }
}