import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Base64;

public class DataSigner {

    public byte[] encryptData(String input) throws Exception {
        byte[] keyBytes = "staticKey1234567".getBytes(StandardCharsets.UTF_8);
        SecretKeySpec key = new SecretKeySpec(keyBytes, "DES");

        Cipher cipher = Cipher.getInstance("DES");
        cipher.init(Cipher.ENCRYPT_MODE, key);

        return cipher.doFinal(input.getBytes(StandardCharsets.UTF_8));
    }

    public String buildReference(String input) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hash = digest.digest(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(hash);
    }

    public String formatLabel(String name) {
        if (name == null || name.isEmpty()) {
            return "default";
        }
        return name.trim();
    }
}