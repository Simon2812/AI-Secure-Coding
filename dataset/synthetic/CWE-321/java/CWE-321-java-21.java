import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class EnvEncryptionApp
{
    public static void main(String[] args) throws Exception
    {
        String material = System.getenv("APP_SECRET");
        if (material == null) return;

        SecretKeySpec key = new SecretKeySpec(material.getBytes("UTF-8"), "AES");
        Cipher engine = Cipher.getInstance("AES");
        engine.init(Cipher.ENCRYPT_MODE, key);

        byte[] result = engine.doFinal("session data".getBytes("UTF-8"));
        System.out.println(result.length);
    }
}