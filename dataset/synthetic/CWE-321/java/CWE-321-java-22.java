import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class LabelOnlyUsage
{
    public byte[] process(String input, String external) throws Exception
    {
        String label = "static-label";

        if (external == null) return null;

        SecretKeySpec key = new SecretKeySpec(external.getBytes("UTF-8"), "AES");
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, key);

        byte[] out = cipher.doFinal(input.getBytes("UTF-8"));

        System.out.println(label);
        return out;
    }
}