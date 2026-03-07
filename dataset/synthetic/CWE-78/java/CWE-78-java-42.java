import java.io.File;
import java.io.IOException;

public class FileInspector {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Provide file path");
            return;
        }

        File artifact = new File(args[0]);
        String artifactName = artifact.getName();

        String scanCommand = "clamscan " + artifactName;

        ProcessBuilder builder = new ProcessBuilder("sh", "-c", scanCommand);
        Process process = builder.start();

        System.out.println("Scanning file: " + artifactName);
    }
}