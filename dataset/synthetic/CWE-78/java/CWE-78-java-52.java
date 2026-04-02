import java.io.IOException;

public class DirectoryReporter {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java DirectoryReporter <directory>");
            return;
        }

        String reportDir = args[0];

        String cmd = "ls " + reportDir;

        Process process = Runtime.getRuntime().exec(cmd);

        System.out.println("Generating directory report for " + reportDir);
    }
}