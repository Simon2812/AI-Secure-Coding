import java.io.IOException;
import java.net.Socket;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class TraceWorker {

    public static void main(String[] args) throws IOException {

        Socket socket = new Socket("localhost", 9091);
        BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));

        String target = reader.readLine();

        if (target == null || !target.matches("[a-zA-Z0-9.-]+")) {
            throw new IllegalArgumentException("Invalid target");
        }

        ProcessBuilder pb = new ProcessBuilder("traceroute", target);
        Process process = pb.start();

        System.out.println("Trace started for " + target);

        reader.close();
        socket.close();
    }
}