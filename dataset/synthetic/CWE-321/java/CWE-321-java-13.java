import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class ReportCipher
{
    public byte[] encrypt(String payload) throws Exception
    {
        String material = "c1a9e7d45b2f8a63";

        SecretKeySpec key = new SecretKeySpec(material.getBytes("UTF-8"), "AES");
        Cipher engine = Cipher.getInstance("AES");
        engine.init(Cipher.ENCRYPT_MODE, key);

        return engine.doFinal(payload.getBytes("UTF-8"));
    }
}