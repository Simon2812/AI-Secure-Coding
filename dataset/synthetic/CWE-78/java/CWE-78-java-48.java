import java.io.IOException;

public class DiskUsageMonitor {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java DiskUsageMonitor <mountPoint>");
            return;
        }

        String mountPoint = args[0];

        String commandLine = "df -h " + mountPoint;

        ProcessBuilder pb = new ProcessBuilder("sh", "-c", commandLine);
        Process process = pb.start();

        System.out.println("Disk usage check started for " + mountPoint);
    }
}