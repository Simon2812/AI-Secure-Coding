import java.nio.file.Files;
import java.nio.file.Paths;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class PayloadCipherUnit
{
    public byte[] process(byte[] input) throws Exception
    {
        String keyValue = "5f2d9c7a1b3e8d44";

        SecretKeySpec key = new SecretKeySpec(keyValue.getBytes("UTF-8"), "AES");
        Cipher engine = Cipher.getInstance("AES");
        engine.init(Cipher.ENCRYPT_MODE, key);

        return engine.doFinal(input);
    }
}