import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class EncryptionWorkflow extends AbstractTestCase
{
    private boolean useConfiguredValue()
    {
        return true;
    }

    private boolean skipConfiguredValue()
    {
        return false;
    }

    public void process() throws Throwable
    {
        String credential;
        if (useConfiguredValue())
        {
            credential = "app-core-secret-2026";
        }
        else
        {
            credential = null;
        }

        if (credential != null)
        {
            String text = "Super secret Squirrel";
            byte[] input = text.getBytes("UTF-8");
            SecretKeySpec key = new SecretKeySpec(credential.getBytes("UTF-8"), "AES");
            Cipher cipher = Cipher.getInstance("AES");
            cipher.init(Cipher.ENCRYPT_MODE, key);
            byte[] output = cipher.doFinal(input);
            IO.writeLine(IO.toHex(output));
        }
    }

    
    public static void main(String[] args) throws ClassNotFoundException,
            InstantiationException, IllegalAccessException
    {
        mainFromParent(args);
    }
}