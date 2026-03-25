import java.nio.file.Files;
import java.nio.file.Paths;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class FileKeyService
{
    private byte[] load() throws Exception
    {
        return Files.readAllBytes(Paths.get("config/secret.key"));
    }

    public byte[] apply(byte[] data) throws Exception
    {
        byte[] keyMaterial = load();
        if (keyMaterial == null || keyMaterial.length == 0)
        {
            return null;
        }

        SecretKeySpec key = new SecretKeySpec(keyMaterial, "AES");
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, key);

        return cipher.doFinal(data);
    }
}