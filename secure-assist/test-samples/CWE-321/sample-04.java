import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class DataEncryptor {
    private static final byte[] SECRET_KEY = "1234567890abcdef".getBytes();

    public static String encrypt(String plaintext) throws Exception {
        SecretKeySpec keySpec = new SecretKeySpec(SECRET_KEY, "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, keySpec);
        return Base64.getEncoder().encodeToString(cipher.doFinal(plaintext.getBytes()));
    }
}
