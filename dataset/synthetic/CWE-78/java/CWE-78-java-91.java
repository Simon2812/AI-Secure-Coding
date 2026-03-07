import java.io.IOException;

public class HostProbe {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java HostProbe <host>");
            return;
        }

        String host = args[0];

        if (!host.matches("[a-zA-Z0-9.-]+")) {
            throw new IllegalArgumentException("Invalid host");
        }

        ProcessBuilder pb = new ProcessBuilder("ping", "-c", "2", host);
        Process process = pb.start();

        System.out.println("Probe started for " + host);
    }
}