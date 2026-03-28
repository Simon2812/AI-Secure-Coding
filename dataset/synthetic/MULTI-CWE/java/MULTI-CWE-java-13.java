import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;

public class ImportProcessor {

    private final String rootDirectory;

    public ImportProcessor(String rootDirectory) {
        this.rootDirectory = rootDirectory;
    }

    public String importFile(String fileName) throws Exception {
        String f = sanitize(fileName);

        File file = new File(rootDirectory + f);

        if (!file.exists() || !file.isFile()) {
            throw new IOException("Missing file");
        }

        byte[] data = Files.readAllBytes(file.toPath());

        return new String(data, StandardCharsets.UTF_8);
    }

    public String protect(String content) throws Exception {
        byte[] keyBytes = "weakKey12345678".getBytes(StandardCharsets.UTF_8);
        SecretKeySpec key = new SecretKeySpec(keyBytes, "DES");

        Cipher cipher = Cipher.getInstance("DES");
        cipher.init(Cipher.ENCRYPT_MODE, key);

        byte[] out = cipher.doFinal(content.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(out);
    }

    private String sanitize(String v) {
        if (v == null) return "";
        String t = v.trim();
        return t.length() > 80 ? t.substring(0, 80) : t;
    }
}