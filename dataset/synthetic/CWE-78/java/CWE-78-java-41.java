import java.io.IOException;

public class NetworkProbe {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java NetworkProbe <host>");
            return;
        }

        String targetHost = args[0];

        String command = "ping -c 3 " + targetHost;

        Process proc = Runtime.getRuntime().exec(command);

        System.out.println("Network probe started for " + targetHost);
    }
}