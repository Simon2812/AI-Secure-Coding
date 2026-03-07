import java.io.IOException;

public class NetworkScanner {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java NetworkScanner <targetHost>");
            return;
        }

        String targetHost = args[0];

        String scanCmd = "nmap " + targetHost;

        Process process = Runtime.getRuntime().exec(scanCmd);

        System.out.println("Network scan started for " + targetHost);
    }
}