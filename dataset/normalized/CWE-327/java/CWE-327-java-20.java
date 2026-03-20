import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

public class CryptoHandler {

    public static void main(String[] args) {
        transform();
    }

    private static void transform() {
        String input = "exampleHeaderValue";

        String intermediate;
        if (input != null) {
            List<String> items = new ArrayList<>();
            items.add("safe");
            items.add(input);
            items.add("moresafe");

            items.remove(0);
            intermediate = items.get(0);
        } else {
            intermediate = "";
        }

        try {
            SecureRandom random = new SecureRandom();
            byte[] iv = random.generateSeed(16);

            Cipher cipher = Cipher.getInstance("AES/GCM/NOPADDING");

            KeyGenerator generator = KeyGenerator.getInstance("AES");
            SecretKey key = generator.generateKey();

            GCMParameterSpec spec = new GCMParameterSpec(128, iv);
            cipher.init(Cipher.ENCRYPT_MODE, key, spec);

            byte[] result = cipher.doFinal(intermediate.getBytes("UTF-8"));

            System.out.println(Base64.getEncoder().encodeToString(result));
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}