import java.security.MessageDigest;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class DerivedKeyProcessor
{
    public byte[] execute(String input) throws Exception
    {
        String base = System.getProperty("user.input");
        if (base == null) return null;

        byte[] digest = MessageDigest.getInstance("SHA-256")
                .digest(base.getBytes("UTF-8"));

        SecretKeySpec key = new SecretKeySpec(digest, "AES");
        Cipher processor = Cipher.getInstance("AES");
        processor.init(Cipher.ENCRYPT_MODE, key);

        return processor.doFinal(input.getBytes("UTF-8"));
    }
}