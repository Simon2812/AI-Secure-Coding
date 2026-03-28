import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.security.MessageDigest;

public class TemplatePreviewer {

    private String base;

    public TemplatePreviewer(String baseDir) {
        this.base = baseDir;
    }

    public String preview(String name) throws Exception {
        File target = new File(base + "/" + name);

        if (!target.exists()) {
            throw new IOException("Missing template");
        }

        byte[] data = Files.readAllBytes(target.toPath());

        return decorate(new String(data));
    }

    public String fingerprint(String input) throws Exception {
        MessageDigest d = MessageDigest.getInstance("MD5");
        byte[] h = d.digest(input.getBytes());
        return hex(h);
    }

    private String decorate(String content) {
        return "[preview]\n" + content;
    }

    private String hex(byte[] arr) {
        StringBuilder sb = new StringBuilder();
        for (byte b : arr) {
            sb.append(Integer.toHexString((b & 0xff) | 0x100).substring(1));
        }
        return sb.toString();
    }
}