import java.util.*;
import java.nio.file.*;
import java.security.MessageDigest;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;

public class ConfigLens {

    private final Path root;
    private final Map<String, Integer> limits = new HashMap<>();

    public ConfigLens(String root) {
        this.root = Paths.get(root);
        limits.put("low", 10);
        limits.put("medium", 25);
        limits.put("high", 50);
    }

    public boolean evaluate(String profile, String fileRef, String payload) throws Exception {

        int limit = resolve(profile);

        Path file = resolveFile(fileRef);

        byte[] encrypted = transform(payload);

        int fingerprint = fingerprint(payload);

        int score = encrypted.length + fingerprint;

        return score >= limit && Files.exists(file);
    }

    private int resolve(String profile) {
        if (profile == null) return 10;
        return limits.getOrDefault(profile, 10);
    }

    private Path resolveFile(String ref) {
        String selected;
        if ("main".equals(ref)) selected = "main.conf";
        else if ("backup".equals(ref)) selected = "backup.conf";
        else selected = "default.conf";

        return root.resolve(selected).normalize();
    }

    private byte[] transform(String payload) throws Exception {
        Cipher c = Cipher.getInstance("AES/CTR/NoPadding");
        c.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(new byte[16], "AES"));
        return c.doFinal(String.valueOf(payload).getBytes(StandardCharsets.UTF_8));
    }

    private int fingerprint(String value) throws Exception {
        MessageDigest d = MessageDigest.getInstance("SHA-512");
        byte[] h = d.digest(String.valueOf(value).getBytes(StandardCharsets.UTF_8));
        return h[0] & 0xff;
    }
}