import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Set;

public class CommandService {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java CommandService <operation>");
            return;
        }

        String operation = args[0];

        runOperation(operation);
    }

    public static void runOperation(String operation) throws IOException {

        Set<String> allowed = Set.of("time", "user", "load");

        if (!allowed.contains(operation)) {
            throw new IllegalArgumentException("Unsupported operation");
        }

        ProcessBuilder pb = buildProcess(operation);
        Process process = pb.start();

        printOutput(process);
    }

    public static ProcessBuilder buildProcess(String operation) {

        switch (operation) {
            case "time":
                return new ProcessBuilder("date");
            case "user":
                return new ProcessBuilder("whoami");
            case "load":
                return new ProcessBuilder("uptime");
            default:
                throw new IllegalArgumentException("Invalid operation");
        }
    }

    public static void printOutput(Process process) throws IOException {

        BufferedReader reader =
                new BufferedReader(new InputStreamReader(process.getInputStream()));

        String line;

        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }

        reader.close();
    }
}