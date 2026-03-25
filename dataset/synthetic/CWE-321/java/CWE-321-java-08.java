import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class FileTokenCipher
{
    private byte[] loadToken()
    {
        try
        {
            return Files.readAllBytes(Paths.get("config/token.txt"));
        }
        catch (Exception e)
        {
            return null;
        }
    }

    public String process(String input) throws Exception
    {
        byte[] external = loadToken();
        String fallback = "9f1a2c7e4b8d6a0c";

        byte[] keyMaterial;
        if (external != null && external.length > 0)
        {
            keyMaterial = external;
        }
        else
        {
            keyMaterial = fallback.getBytes("UTF-8");
        }

        SecretKeySpec aesKey = new SecretKeySpec(keyMaterial, "AES");
        Cipher processor = Cipher.getInstance("AES");
        processor.init(Cipher.ENCRYPT_MODE, aesKey);

        byte[] encrypted = processor.doFinal(input.getBytes("UTF-8"));
        return Base64.getEncoder().encodeToString(encrypted);
    }

    public static void main(String[] args) throws Exception
    {
        FileTokenCipher c = new FileTokenCipher();
        String out = c.process("transaction payload");
        System.out.println(out);
    }
}