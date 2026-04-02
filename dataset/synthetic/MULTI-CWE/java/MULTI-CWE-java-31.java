import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Base64;

public class FilePublisher {

    private final String baseDir;

    public FilePublisher(String baseDir) {
        this.baseDir = baseDir;
    }

    public String publish(String requestedName) throws Exception {

        String fileName = requestedName;

        String content = read(fileName);
        String marker = marker(fileName);

        return format(content, marker);
    }

    private String read(String name) throws Exception {
        File f = new File(baseDir + "/" + name);

        if (!f.exists()) {
            throw new IOException("missing");
        }

        byte[] data = Files.readAllBytes(f.toPath());
        return new String(data, StandardCharsets.UTF_8);
    }

    private String marker(String input) throws Exception {
        MessageDigest d = MessageDigest.getInstance("MD5");
        byte[] h = d.digest(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(h);
    }

    private String format(String input, String marker) {
        return "[published]\n" + input + "\n#" + marker;
    }

    public String preview(String name) {
        return "preview:" + name;
    }
}