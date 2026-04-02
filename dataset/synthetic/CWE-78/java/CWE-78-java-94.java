import java.io.IOException;
import java.util.Set;

public class ScriptExecutor {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java ScriptExecutor <script>");
            return;
        }

        String script = args[0];

        Set<String> allowedScripts = Set.of("backup.sh", "cleanup.sh", "status.sh");

        if (!allowedScripts.contains(script)) {
            throw new IllegalArgumentException("Unsupported script");
        }

        ProcessBuilder pb = new ProcessBuilder("sh", script);
        Process process = pb.start();

        System.out.println("Script executed: " + script);
    }
}