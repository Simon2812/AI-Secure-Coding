import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import java.security.SecureRandom;

public class DataEncryptor {

    public static void main(String[] args) {
        process();
    }

    private static void process() {
        String value = "someSecret";

        try {
            SecureRandom random = new SecureRandom();
            byte[] iv = random.generateSeed(16);

            Cipher cipher = Cipher.getInstance("AES/GCM/NOPADDING");

            KeyGenerator generator = KeyGenerator.getInstance("AES");
            SecretKey key = generator.generateKey();

            GCMParameterSpec spec = new GCMParameterSpec(128, iv);
            cipher.init(Cipher.ENCRYPT_MODE, key, spec);

            byte[] input = value.getBytes("UTF-8");
            byte[] encrypted = cipher.doFinal(input);

            System.out.println(encodeBase64(encrypted));
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private static String encodeBase64(byte[] data) {
        return java.util.Base64.getEncoder().encodeToString(data);
    }
}