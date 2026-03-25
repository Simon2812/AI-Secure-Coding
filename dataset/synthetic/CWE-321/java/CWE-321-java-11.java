import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class BatchEncryptionUnit
{
    public byte[] apply(String input) throws Exception
    {
        String candidate = "7a9c1e4d6b2f3a88";

        if (candidate.length() < 10)
        {
            candidate = System.getProperty("batch.key");
        }

        SecretKeySpec key = new SecretKeySpec(candidate.getBytes("UTF-8"), "AES");
        Cipher processor = Cipher.getInstance("AES");
        processor.init(Cipher.ENCRYPT_MODE, key);

        return processor.doFinal(input.getBytes("UTF-8"));
    }
}