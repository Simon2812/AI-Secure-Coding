import java.io.IOException;

public class DirectoryList {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java DirectoryList <path>");
            return;
        }

        String path = args[0];

        if (!path.matches("[a-zA-Z0-9._/\\-]+")) {
            throw new IllegalArgumentException("Invalid path");
        }

        ProcessBuilder pb = new ProcessBuilder("ls", path);
        Process process = pb.start();

        System.out.println("Listing directory: " + path);
    }
}