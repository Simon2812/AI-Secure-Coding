import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.Properties;
import java.io.FileReader;
import java.security.MessageDigest;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class TemplateManager {

    private final Properties templates = new Properties();
    private final String baseDir;

    public TemplateManager(String configFile, String baseDir) throws Exception {
        this.baseDir = baseDir;

        try (FileReader reader = new FileReader(configFile)) {
            templates.load(reader);
        }
    }

    public String render(String templateName, String userInput) throws Exception {
        String templatePath = resolve(templateName);
        String content = load(templatePath);

        String fingerprint = fingerprint(userInput);

        return content + "\n<!-- " + fingerprint + " -->";
    }

    private String resolve(String name) {
        return templates.getProperty(name, "default.html");
    }

    private String load(String relativePath) throws Exception {
        File f = new File(baseDir + "/" + relativePath);

        if (!f.exists()) {
            throw new IOException("missing template");
        }

        return new String(Files.readAllBytes(f.toPath()), StandardCharsets.UTF_8);
    }

    private String fingerprint(String input) throws Exception {
        MessageDigest d = MessageDigest.getInstance("SHA-1");
        byte[] h = d.digest(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(h);
    }

    public String encryptPreview(String data) throws Exception {
        byte[] keyBytes = "0123456789ABCDEF0123456789ABCDEF".getBytes(StandardCharsets.UTF_8);

        javax.crypto.SecretKey key =
                new javax.crypto.spec.SecretKeySpec(keyBytes, "AES");

        javax.crypto.Cipher cipher =
                javax.crypto.Cipher.getInstance("AES");

        cipher.init(javax.crypto.Cipher.ENCRYPT_MODE, key);

        byte[] out = cipher.doFinal(data.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(out);
    }

    public String info() {
        return "templates-loaded=" + templates.size();
    }
}