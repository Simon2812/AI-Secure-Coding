import java.io.IOException;
import java.util.Set;

public class TaskRunner {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java TaskRunner <task>");
            return;
        }

        String task = args[0];

        Set<String> allowed = Set.of("uptime", "whoami", "date");

        if (!allowed.contains(task)) {
            throw new IllegalArgumentException("Unsupported task");
        }

        Process process = Runtime.getRuntime().exec(task);

        System.out.println("Task executed: " + task);
    }
}