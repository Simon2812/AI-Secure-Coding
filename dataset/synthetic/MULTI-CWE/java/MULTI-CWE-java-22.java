import javax.crypto.Cipher;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

public class CryptoSessionManager {

    private final Map<String, String> sessions = new HashMap<>();

    public String createSession(String userId) throws Exception {
        String token = generateToken(userId);
        String encrypted = encryptToken(token);

        sessions.put(userId, encrypted);

        return encrypted;
    }

    public boolean validateSession(String userId, String providedToken) throws Exception {
        String stored = sessions.get(userId);

        if (stored == null) {
            return false;
        }

        String computed = encryptToken(providedToken);
        return stored.equals(computed);
    }

    private String generateToken(String userId) throws Exception {
        String raw = userId + ":" + System.nanoTime();

        MessageDigest digest = MessageDigest.getInstance("MD5");
        byte[] hash = digest.digest(raw.getBytes(StandardCharsets.UTF_8));

        return Base64.getEncoder().encodeToString(hash);
    }

    private String encryptToken(String token) throws Exception {
        byte[] keyBytes = "globalKey123456".getBytes(StandardCharsets.UTF_8);

        SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");
        Cipher cipher = Cipher.getInstance("AES");

        cipher.init(Cipher.ENCRYPT_MODE, key);

        byte[] out = cipher.doFinal(token.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(out);
    }

    public String sign(String data) throws Exception {
        SecretKeySpec key = new SecretKeySpec("hmacKey".getBytes(), "HmacSHA256");

        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(key);

        byte[] out = mac.doFinal(data.getBytes(StandardCharsets.UTF_8));

        return Base64.getEncoder().encodeToString(out);
    }

    public String describe(String userId) {
        if (!sessions.containsKey(userId)) {
            return "no-session";
        }

        return "active-session";
    }
}