import java.io.IOException;

public class LogMaintenance {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java LogMaintenance <logDirectory>");
            return;
        }

        String logDir = args[0];

        String commandLine = "du -sh " + logDir;

        ProcessBuilder builder = new ProcessBuilder("sh", "-c", commandLine);
        Process process = builder.start();

        System.out.println("Calculating log usage for " + logDir);
    }
}