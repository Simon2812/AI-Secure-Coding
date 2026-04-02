import java.io.IOException;
import java.util.List;

public class CommandDispatcher {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java CommandDispatcher <action>");
            return;
        }

        String action = args[0];

        List<String> command;

        switch (action) {
            case "time":
                command = List.of("date");
                break;
            case "user":
                command = List.of("whoami");
                break;
            case "load":
                command = List.of("uptime");
                break;
            default:
                throw new IllegalArgumentException("Unsupported action");
        }

        ProcessBuilder pb = new ProcessBuilder(command);
        Process process = pb.start();

        System.out.println("Action executed: " + action);
    }
}