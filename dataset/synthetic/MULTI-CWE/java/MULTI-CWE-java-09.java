import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.security.MessageDigest;
import java.util.Base64;

public class TemplateLoader {

    private static final String BASE_DIR = "/var/app/templates/";

    public String loadTemplate(String name) throws Exception {
        String normalized = normalize(name);

        File file = new File(BASE_DIR + normalized);

        if (!file.exists() || !file.isFile()) {
            throw new IOException("Template not found");
        }

        byte[] content = Files.readAllBytes(file.toPath());

        logAccess(normalized);

        return new String(content);
    }

    private String normalize(String input) {
        if (input == null) {
            return "default.html";
        }

        String trimmed = input.trim();

        if (trimmed.isEmpty()) {
            return "default.html";
        }

        if (trimmed.length() > 80) {
            return trimmed.substring(0, 80);
        }

        return trimmed;
    }

    private void logAccess(String name) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("MD5");
        byte[] hash = digest.digest(name.getBytes());
        String tag = Base64.getEncoder().encodeToString(hash);
        System.out.println("access=" + tag);
    }
}