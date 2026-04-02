import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import java.util.Base64;

public class TokenService {

    public String protect(String input) {
        try {
            Cipher cipher = Cipher.getInstance("RC4");

            KeyGenerator generator = KeyGenerator.getInstance("RC4");
            SecretKey key = generator.generateKey();

            cipher.init(Cipher.ENCRYPT_MODE, key);

            byte[] data = input.getBytes("UTF-8");
            byte[] encrypted = cipher.doFinal(data);

            return Base64.getEncoder().encodeToString(encrypted);
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }

    public static void main(String[] args) {
        TokenService service = new TokenService();
        System.out.println(service.protect("sample-data"));
    }
}