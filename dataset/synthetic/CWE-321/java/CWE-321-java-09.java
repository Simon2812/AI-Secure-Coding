import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class InlineEncryptionProcessor
{
    public byte[] transform(String input) throws Exception
    {
        String material = System.getProperty("runtime.key");

        if (material == null || material.isEmpty())
        {
            material = "a94f3c2b7d6e1f08";
        }

        byte[] keyBytes = material.getBytes("UTF-8");

        SecretKeySpec runtimeKey = new SecretKeySpec(keyBytes, "AES");
        Cipher engine = Cipher.getInstance("AES");
        engine.init(Cipher.ENCRYPT_MODE, runtimeKey);

        return engine.doFinal(input.getBytes("UTF-8"));
    }

    public static void main(String[] args) throws Exception
    {
        InlineEncryptionProcessor processor = new InlineEncryptionProcessor();
        byte[] out = processor.transform("audit log entry");
        System.out.println(out.length);
    }
}