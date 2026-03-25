import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class ConsoleEncryption
{
    public byte[] run() throws Exception
    {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String value = reader.readLine();

        if (value == null || value.isEmpty())
        {
            return null;
        }

        SecretKeySpec key = new SecretKeySpec(value.getBytes("UTF-8"), "AES");
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, key);

        return cipher.doFinal("user payload".getBytes("UTF-8"));
    }
}