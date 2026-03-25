import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class RuntimeEncryptionHandler extends AbstractTestCase
{
    private static final boolean usePrimary = true;
    private static final boolean useAlternate = false;

    public void handle() throws Throwable
    {
        String credential;
        if (useAlternate)
        {
            credential = null;
        }
        else
        {
            credential = "";
            try
            {
                InputStreamReader reader = new InputStreamReader(System.in, "UTF-8");
                BufferedReader buffer = new BufferedReader(reader);
                credential = buffer.readLine();
            }
            catch (IOException e)
            {
                IO.logger.log(Level.WARNING, "Error with stream reading", e);
            }
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