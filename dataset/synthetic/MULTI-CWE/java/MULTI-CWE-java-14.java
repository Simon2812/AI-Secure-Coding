import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Base64;

public class SessionTokenManager {

    private static final String SECRET = "globalStaticKey";

    public String encode(String userId) throws Exception {
        SecretKeySpec key = new SecretKeySpec(SECRET.getBytes(StandardCharsets.UTF_8), "AES");
        Cipher cipher = Cipher.getInstance("AES");

        cipher.init(Cipher.ENCRYPT_MODE, key);

        byte[] encrypted = cipher.doFinal(userId.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(encrypted);
    }

    public String buildToken(String userId) throws Exception {
        String payload = userId + ":" + System.currentTimeMillis();

        MessageDigest digest = MessageDigest.getInstance("MD5");
        byte[] hash = digest.digest(payload.getBytes(StandardCharsets.UTF_8));

        return Base64.getEncoder().encodeToString(hash);
    }

    public String normalize(String v) {
        if (v == null) return "";
        String t = v.trim();
        return t.length() > 64 ? t.substring(0, 64) : t;
    }
}