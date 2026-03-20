import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import java.security.SecureRandom;
import java.util.Base64;

public class SecureFlow {

    public static void main(String[] args) {
        handle();
    }

    private static void handle() {
        String headerName = "customHeader";

        StringBuilder builder = new StringBuilder(headerName);
        String prepared = builder.append("_SafeStuff").toString();

        try {
            Cipher cipher = buildCipher();

            byte[] input = prepared.getBytes("UTF-8");
            byte[] encrypted = cipher.doFinal(input);

            System.out.println(Base64.getEncoder().encodeToString(encrypted));
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private static Cipher buildCipher() throws Exception {
        SecureRandom random = new SecureRandom();
        byte[] iv = random.generateSeed(16);

        Cipher cipher = Cipher.getInstance("AES/GCM/NOPADDING");

        KeyGenerator generator = KeyGenerator.getInstance("AES");
        SecretKey key = generator.generateKey();

        GCMParameterSpec spec = new GCMParameterSpec(128, iv);
        cipher.init(Cipher.ENCRYPT_MODE, key, spec);

        return cipher;
    }
}
