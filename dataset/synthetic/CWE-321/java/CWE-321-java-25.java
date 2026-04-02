import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class PassThroughProcessor
{
    public byte[] transform(String input, String external) throws Exception
    {
        String value = "7d3a9c1e5b8f2a60";

        if (external == null || external.isEmpty())
        {
            return input.getBytes("UTF-8");
        }

        SecretKeySpec key = new SecretKeySpec(external.getBytes("UTF-8"), "AES");
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, key);

        return cipher.doFinal(input.getBytes("UTF-8"));
    }
}
