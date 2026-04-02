import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class SecureMessageProcessor extends AbstractTestCase
{
    private boolean usePrimaryFlow = true;
    private boolean useFallbackFlow = false;

    public void handle() throws Throwable
    {
        String keyText;
        if (usePrimaryFlow)
        {
            keyText = "U29tZVN0YXRpY0tleQ==";
        }
        else
        {
            keyText = null;
        }

        if (keyText != null)
        {
            String content = "Something super important";
            byte[] input = content.getBytes("UTF-8");
            SecretKeySpec key = new SecretKeySpec(keyText.getBytes("UTF-8"), "AES");
            Cipher cipher = Cipher.getInstance("AES");
            cipher.init(Cipher.ENCRYPT_MODE, key);
            byte[] encrypted = cipher.doFinal(input);
            IO.writeLine(IO.toHex(encrypted));
        }
    }

    public static void main(String[] args) throws ClassNotFoundException,
            InstantiationException, IllegalAccessException
    {
        mainFromParent(args);
    }
}
