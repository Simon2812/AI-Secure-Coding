import java.io.IOException;

public class ArchiveCreator {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java ArchiveCreator <directory>");
            return;
        }

        String archiveSource = args[0];

        String archiveCommand = "tar -cf backup.tar " + archiveSource;

        ProcessBuilder builder = new ProcessBuilder("sh", "-c", archiveCommand);
        Process process = builder.start();

        System.out.println("Archive process started for " + archiveSource);
    }
}